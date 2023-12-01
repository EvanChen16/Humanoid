
/* Example application of Columbo Simple Serial Library
 * Copyright 2003 Marcin Siennicki <m.siennicki@cloos.pl>
 * see COPYING file for details */

#include <stdio.h>
#include <unistd.h>

#include "cssl.h"


/* if it is time to finish */
static int finished=0;


/* example callback, it gets its id, buffer, and buffer length */
static void callback(int id,
                     uint8_t *buf,
                     int length) {
    int i;

    printf("Received data: ");

    for (i = 0; i < length; i++) {
        putchar(buf[i]);
    }

    fflush(stdout);
}



int main()
{
    cssl_t *serial;

    cssl_start();
    printf("Columbo Simple Serial Library test\n");
    serial = cssl_open("/dev/ttyUSB0", callback, 0, 115200, 8, 0, 1);
    if (!serial) {
        printf("Failed to open serial port!\n");
        printf("%s\n", cssl_geterrormsg());
        return -1;
    } else {
        printf("Serial port opened successfully!\n");
    }

    cssl_putstring(serial,"Type some data, ^D finishes.");

    while (!finished)
	pause();

    printf("\n^D - we exit\n");

    cssl_close(serial);
    cssl_stop();

    return 0;
}
