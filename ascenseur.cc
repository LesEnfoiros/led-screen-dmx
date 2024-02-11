// 
// ASCENSEUR, BY ENFOIROS
//
// Author: Damien MOLINA
// Date: 2023-12-03
//
#include "led-matrix.h"
#include "graphics.h"

#include <getopt.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <vector>
#include <string>
#include <thread>
#include <iostream>
#include <wiringPiI2C.h>
#include <chrono>

using namespace rgb_matrix ;
using namespace std ;

// =============================================
//               MAIN CONSTANTS
// =============================================
// Found here: https://github.com/fcambus/spleen
#define FONT_BDF    "./assets/font-32x64.bdf"
#define ARROW_WIDTH 30
#define SECONDS_BETWEEN_FRAMES 1

// DMX CONSTANTS
#define DMX_I2C_ID          0x08
#define DMX_NUMBER_CHANNELS 3
#define DMX_CHANNEL_COLOR_R 0
#define DMX_CHANNEL_COLOR_G 1
#define DMX_CHANNEL_COLOR_B 2
#define DMX_CHANNEL_COLOR_ONOFF    3
#define DMX_CHANNEL_COLOR_BULLSHIT 4
#define DMX_CHANNEL_COLOR_ORDER    5


namespace enfoiros {
    // Interrupt logic for stopping the rendering loop.
    volatile bool interrupt_received = false;
    static void InterruptHandler(int signo) {
        interrupt_received = true;
    }

    /**
     * Display how to use this software to the user.
     * 
     * @param char *progname
     */
    static int usage(const char *progname) {
        fprintf(stderr, "usage: %s [options]\n", progname) ;
        fprintf(stderr, "Reads text from stdin and displays it. Empty string: clear screen\n") ;
        fprintf(stderr, "Options:\n") ;
        fprintf(stderr,
            "\t-d <time-format>  : Default '%%H:%%M'. See strftime()\n"
            "\t                    Can be provided multiple times for multiple "
            "lines\n"
            "\t-f <font-file>    : Use given font.\n"
            "\t-x <x-origin>     : X-Origin of displaying text (Default: 0)\n"
            "\t-y <y-origin>     : Y-Origin of displaying text (Default: 0)\n"
            "\t-s <line-spacing> : Extra spacing between lines when multiple -d given\n"
            "\t-S <spacing>      : Extra spacing between letters (Default: 0)\n"
            "\t-C <r,g,b>        : Color. Default 255,255,0\n"
            "\t-B <r,g,b>        : Background-Color. Default 0,0,0\n"
            "\t-O <r,g,b>        : Outline-Color, e.g. to increase contrast.\n"
            "\n"
        ) ;
        
        return 1 ;
    }

    class Screen {
        public:
            Color font_color ;
            Color bg_color ;
            rgb_matrix::Font font ;
            FrameCanvas *canvas ;
            RGBMatrix *matrix ;
            RGBMatrix::Options matrix_options ;
            rgb_matrix::RuntimeOptions runtime_opt ;
            struct timespec next_time ;

            Screen() {
                this->font_color = Color(255, 255, 255) ;
                this->bg_color = Color(0, 0, 0) ;
            }

            int build(int argc, char *argv[]) {
                // If the args are invalid.
                if(! rgb_matrix::ParseOptionsFromFlags(&argc, &argv, &matrix_options, &runtime_opt)) {
                    return usage(argv[0]) ;
                }

                // Load font. This needs to be a filename with a bdf bitmap font.
                if(! font.LoadFont(FONT_BDF)) {
                    fprintf(stderr, "Couldn't load font '%s'\n", FONT_BDF) ;
                    return 1 ;
                }

                matrix = RGBMatrix::CreateFromOptions(matrix_options, runtime_opt);
                if(matrix == NULL) {
                    return 1 ;
                }

                this->canvas = this->matrix->CreateFrameCanvas() ;
                this->canvas->Fill(this->bg_color.r, this->bg_color.g, this->bg_color.b) ;

                // Initialize the interuption handlers.
                signal(SIGTERM, enfoiros::InterruptHandler) ;
                signal(SIGINT, enfoiros::InterruptHandler) ;

                // Initialize the clock helper.
                this->next_time.tv_sec = time(NULL) ;
                this->next_time.tv_nsec = 0 ;

                return 0 ;
            }

            /**
             * This function is moving the frame to the next
             * time it will be calculated.
             * 
             * @return void
             */
            void nextFrame() {
                // Saying that the next rendering phase will be in 1 second.
                //this->next_time.tv_sec += 1 ;
                this->next_time.tv_nsec += 500 * 1000 * 1000 ;

                // Wait until we're ready to show it.
                clock_nanosleep(CLOCK_REALTIME, TIMER_ABSTIME, &(this->next_time), NULL) ;

                // Atomic swap with double buffer
                this->canvas = this->matrix->SwapOnVSync(this->canvas) ;

                // We clear the screen to be rendered again;
                this->canvas->Fill(this->bg_color.r, this->bg_color.g, this->bg_color.b) ;
            }

            /**
             * Clean the screen before ending the software.
             * 
             * @return void
             */
            void clean() {
                // Finished. Shut down the RGB matrix.
                delete this->matrix ;

                write(STDOUT_FILENO, "\n", 1) ;  // Create a fresh new line after ^C on screen
            }
    } ;

    class Ascenseur {
        private:
            void _drawText(int x, int y, char * text) {
                rgb_matrix::DrawText(this->screen->canvas, this->screen->font, x, y, this->screen->font_color, &(this->screen->bg_color), text, 0) ;
            }

            void _drawPixel(int x, int y) {
                this->screen->canvas->SetPixel(x, y, this->screen->font_color.r, this->screen->font_color.g, this->screen->font_color.b) ;
            }
							
        public:
            // Screen variables.
            Screen *screen ;
            int orig_x ;
            int orig_y ;

            // Ascenseur variables.
            int current_stair = 0 ;
            int target_stair = 0 ;
            int animation_next_frame = 0 ;
            bool is_hors_service = false ;						


            /**
             * Build a new Ascenseur instance.
             * 
             * @param int orig_x
             * @param int orig_y
             */
            Ascenseur(Screen *screen, int orig_x, int orig_y) {
                this->screen = screen ;
                this->orig_x = orig_x ;
                this->orig_y = orig_y ;
            }

            /**
             * This function draws an arrow in the given location.
             * 
             * @param int orig_x: horizontal origin of the arrow
             * @param int orig_y: vertical origin. Will be the "topest" value of the arrow.
             * @param top_to_down: orientation of the arrow
            */
            void drawArrow() {
                if(this->current_stair == this->target_stair || this->is_hors_service) {
                    return ;
                }

                bool top_to_down = this->target_stair < this->current_stair ;
                int multiplier = top_to_down ? 1 : -1 ;
                int head_orig_y = this->orig_y + (top_to_down ? 0 : 64) ;

                for(int y = 0 ; y < ARROW_WIDTH ; y++) {
                    for(int x = y ; x < ARROW_WIDTH - y ; x++) {
                        this->_drawPixel(orig_x + x, head_orig_y + multiplier * 2 * y) ;
                        this->_drawPixel(orig_x + x, head_orig_y + multiplier * 2 * y + multiplier) ;
                    }
                }
            }

            /**
             * Draw the given stair level.
             * 
             * @param int level
             */
            void drawStairLevel() {
                if(this->is_hors_service) {
                    int random = rand() % 10 ;

                    // This is done to make the "HS" text "strobbing".""
                    if(random == 7) {
                        this->_drawText(0, this->screen->font.baseline(), (char *) "H") ;
                    } else if(random == 2) {
                        this->_drawText(0, this->screen->font.baseline(), (char *) " S") ;
                    } else if(rand() % 10 != 9) {
                        this->_drawText(0, this->screen->font.baseline(), (char *) "HS") ;
                    }

                    return ;
                }

                int current_time = (int) time(NULL) ;

                if(this->current_stair != this->target_stair && current_time >= this->animation_next_frame) {
                    this->current_stair += this->current_stair > this->target_stair ? -1 : 1 ;
                    this->animation_next_frame = SECONDS_BETWEEN_FRAMES + (int) time(NULL) ;
                }

                int level = this->current_stair ;

                // This is required for not rendering
                // levels with more characters than allowed.
                if(level > 9 || level < -9) {
                    fprintf(stderr, "Couldn't display level '%d'\n", level) ;
                    
                    return ;
                }

                int is_negative = level < 0 ;
                level = is_negative ? -level : level ;

                char str[5] ;
                sprintf(str, "%d", level) ;
                str[4] = 0 ;

                // Print the stair level.
                this->_drawText(36, this->screen->font.baseline(), str) ;

                // If the number is negative, then print a "minus" sign.
                if(is_negative) {
                    int height = 28 ;

                    for(int x = 20 ; x < 34 ; x++) {
                        this->_drawPixel(x, height) ;
                        this->_drawPixel(x, height + 1) ;
                        this->_drawPixel(x, height + 2) ;
                    }
                }
            }
    } ;
} ;

// =============================================
//               MAIN CONSTANTS
// =============================================
enfoiros::Screen screen ;

// DMX.
int dmx_fd ;

/**
 * This function set the ascenseur parameter to go
 * to the required level.
 * 
 * @param ascenseur ascenseur
 * @param int level
 */
void go_to_stair(enfoiros::Ascenseur * ascenseur, int level) {
    if(ascenseur->current_stair == level || ascenseur->target_stair == level) {
        return ;
    }

    ascenseur->is_hors_service = false ;
    ascenseur->target_stair = level ;
    ascenseur->animation_next_frame = SECONDS_BETWEEN_FRAMES + (int) time(NULL) ;
}

/**
 * Make the thread manage the orders received
 * from the Arduino / DMX signal.
 * 
 * @param Ascenseur * ascenseur
 * @param int order
 */
void thread_manage_order(enfoiros::Ascenseur * ascenseur, int order) {
    // Upper stairs.
    if(order >= 0 && order < 10) {
        go_to_stair(ascenseur, 5) ;
    } else if(order >= 10 && order < 20) {
        go_to_stair(ascenseur, 4) ;
    } else if(order >= 20 && order < 30) {
        go_to_stair(ascenseur, 3) ;
    } else if(order >= 30 && order < 40) {
        go_to_stair(ascenseur, 2) ;
    } else if(order >= 40 && order < 50) {
        go_to_stair(ascenseur, 1) ;
    } else if(order >= 50 && order < 60) {
        go_to_stair(ascenseur, 0) ;
    } 
    
    // Lower stairs.
    else if(order >= 60 && order < 70) {
        go_to_stair(ascenseur, -1) ;
    } else if(order >= 70 && order < 80) {
        go_to_stair(ascenseur, -2) ;
    } else if(order >= 80 && order < 90) {
        go_to_stair(ascenseur, -3) ;
    } else if(order >= 90 && order < 100) {
        go_to_stair(ascenseur, -4) ;
    } else if(order >= 100 && order < 110) {
        go_to_stair(ascenseur, -5) ;
    } 
    
    // HS animation.
    else if(order >= 110 && order < 120) {
        ascenseur->is_hors_service = true ;
        ascenseur->current_stair = ascenseur->target_stair ;
    }
}

/**
 * Read the DMX value of the given channel.
 * 
 * @param int channel
 * @return int
*/
int read_dmx_value(int channel) {
    wiringPiI2CWrite(dmx_fd, channel);

    return wiringPiI2CRead(dmx_fd) ;
}

/**
 * This function is executed by a thread to retrieve the
 * value of the DMX shield without blocking the rendering loop.
 * 
 * @param ascenseur ascenseur
 */
void thread_listening_on_dmx(enfoiros::Ascenseur * ascenseur) {
    Color * color_buffer = new Color(
        ascenseur->screen->font_color.r, ascenseur->screen->font_color.g, ascenseur->screen->font_color.b
    ) ;

    while(1) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100)) ;
        
        int on_off = read_dmx_value(DMX_CHANNEL_COLOR_ONOFF) ;

        // If we receive the order to hide the elevator
        // display, then stop the loop here.
        if(on_off > 120) {
            std::cout << "On/Off: " << on_off << "\n" ;
            //continue ;
        }

        // Manage the order.
        int order = read_dmx_value(DMX_CHANNEL_COLOR_ORDER) ;
        thread_manage_order(ascenseur, order) ;

        int bullshit = read_dmx_value(DMX_CHANNEL_COLOR_BULLSHIT) ;
        // TODO

        // Manage the font color: red.
        int font_r = read_dmx_value(DMX_CHANNEL_COLOR_R) ;
        if(color_buffer->r == font_r) {
            ascenseur->screen->font_color.r = font_r ;
        } else {
            color_buffer->r = font_r ;
        }

        // Manage the font color: green.
        int font_g = read_dmx_value(DMX_CHANNEL_COLOR_G) ;
        if(color_buffer->g == font_g) {
            ascenseur->screen->font_color.g = font_g ;
        } else {
            color_buffer->g = font_g ;
        }

        // Manage the font color: blue.
        int font_b = read_dmx_value(DMX_CHANNEL_COLOR_B) ;
        if(color_buffer->b == font_b) {
            ascenseur->screen->font_color.b = font_b ;
        } else {
            color_buffer->b = font_b ;
        }

        std::cout << "(" << font_r << ", " << font_g << ", " << font_b << ") => " << order << "\n" ;
    }
}

/**
 * Main software entry point.
 * 
 * @param int argc
 * @param char *argv[]
 * @return int
 */
int main(int argc, char *argv[]) {
    // Setup the DMX I2C.
    dmx_fd = wiringPiI2CSetup(0x08) ;

    // Check the I2C setup.
    if(dmx_fd == -1) {
        std::cout << "Failed to init I2C communication.\n" ;
        return -1 ;
    }

    std::cout << "I2C communication successfully setup.\n" ;

    screen = enfoiros::Screen() ;

    // If building failed, then stop the software here.
    if(screen.build(argc, argv) != 0) {
        return 1 ;
    }

    enfoiros::Ascenseur ascenseur = enfoiros::Ascenseur(&screen, 0, 0) ;
    thread t1(thread_listening_on_dmx, &ascenseur) ;

    while(! enfoiros::interrupt_received) {
        ascenseur.drawArrow() ;
        ascenseur.drawStairLevel() ;

        screen.nextFrame() ;
    }

    screen.clean() ;

    return 0 ;
}

