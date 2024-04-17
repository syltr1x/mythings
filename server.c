#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")
#define DEFAULT_PORT 80
#define DEFAULT_BUFLEN 1024

void sendFile(SOCKET clientSocket, const char* filePath) {
    FILE* file = fopen(filePath, "rb");
    if (file == NULL) {
        printf("Error opening file: %s\n", filePath);
        return;
    }

    fseek(file, 0, SEEK_END);
    long fileSize = ftell(file);
    fseek(file, 0, SEEK_SET);
    char* fileBuffer = (char*)malloc(fileSize);
    if (fileBuffer == NULL) {
        printf("Memory allocation error\n");
        fclose(file);
        return;
    }
    fread(fileBuffer, 1, fileSize, file);
    fclose(file);

    char httpResponse[1024];
    sprintf(httpResponse, "HTTP/1.1 200 OK\r\nContent-Length: %ld\r\nContent-Type: application/octet-stream\r\n\r\n", fileSize);
    send(clientSocket, httpResponse, strlen(httpResponse), 0);
    send(clientSocket, fileBuffer, fileSize, 0);

    free(fileBuffer);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <file_to_share>\n", argv[0]);
        return 1;
    }
    WSADATA wsaData;
    SOCKET listenSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;
    int addrLen = sizeof(clientAddr);

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup failed.\n");
        return 1;
    }
    if ((listenSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)) == INVALID_SOCKET) {
        printf("Error creating socket: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serverAddr.sin_port = htons(DEFAULT_PORT);
    if (bind(listenSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
        printf("Bind failed with error: %d\n", WSAGetLastError());
        closesocket(listenSocket);
        WSACleanup();
        return 1;
    }
    if (listen(listenSocket, SOMAXCONN) == SOCKET_ERROR) {
        printf("Listen failed with error: %d\n", WSAGetLastError());
        closesocket(listenSocket);
        WSACleanup();
        return 1;
    }

    printf("Server is listening on port %d\n", DEFAULT_PORT);
    printf("Sharing file: %s\n", argv[1]);
    while (1) {
        if ((clientSocket = accept(listenSocket, (struct sockaddr*)&clientAddr, &addrLen)) == INVALID_SOCKET) {
            printf("Accept failed with error: %d\n", WSAGetLastError());
            closesocket(listenSocket);
            WSACleanup();
            return 1;
        }
        sendFile(clientSocket, argv[1]);
        closesocket(clientSocket);
    }
    closesocket(listenSocket);
    WSACleanup();

    return 0;
}
