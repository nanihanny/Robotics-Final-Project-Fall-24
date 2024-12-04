#ifndef DATA_TRANSFER_H
#define DATA_TRANSFER_H

#include <WiFiNINA.h>
#include <HttpClient.h>

// Declare the server's address and port
extern const char server1[];
extern const char server2[];

// Declare the global client and http objects
extern WiFiClient client1;
extern HttpClient http1;
extern WiFiClient client2;
extern HttpClient http2;

// Function declarations
void send_data1(String data);
void send_data2(String data);
String get_data1();
String get_data2();

#endif  // DATA_TRANSFER_H
