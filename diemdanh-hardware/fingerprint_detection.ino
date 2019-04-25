#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>
#include <ESP8266WiFi.h>

// configuration
// WiFi config
const char* ssid = "ABX-AP";
const char* password = "fiisoft.net";

// server to connect to
const char* host = "httpbin.org";

SoftwareSerial mySerial(4,5);
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

int  R = 13;
int  G = 15;

void connectToWifi()
{
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
}


void sendFigerprintToServer(uint8_t fingerprint_id)
{
  WiFiClient client;

  Serial.printf("\n[Connecting to %s ... ", host);
  if (client.connect(host, 80))
  {
    Serial.println("connected]");

    Serial.println("[Sending a request]");
    client.print(String("GET /check/") + fingerprint_id + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );

    Serial.println("[Response:]");
    while (client.connected() || client.available())
    {
      if (client.available())
      {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
    }
    client.stop();
    Serial.println("\n[Disconnected]");
  }
  else
  {
    Serial.println("connection failed!]");
    client.stop();
  }
}

void onLed(int i)
{
  digitalWrite(i, HIGH);
  delay (500);
}

void offLed(int i)
{
  digitalWrite(i, LOW);
//  delay (300);
}

void OnOff(int i)
{
    onLed(i);
    offLed(i);
}

void nhapnhay(int i, int k)
{
    do {
      onLed(i);
      delay(30);
      offLed(i);
      delay(30);
      k--;
    } while (k > 0);
}
void setup() {
  s.begin(9600);
  Serial.begin(9600);
  connectToWifi();
  pinMode(R, OUTPUT);//den do
  pinMode(G, OUTPUT);//den xanh
  while (!Serial);  // For Yun/Leo/Micro/Zero/...
  delay(100);
  Serial.println("\n\nAdafruit finger detect test");
  // set the data rate for the sensor serial port
  finger.begin(57600);
  if (finger.verifyPassword()) {
    Serial.println("Found fingerprint sensor!");
    nhapnhay(G,3);
  }
  else {
    Serial.println("Did not find fingerprint sensor :(");
    nhapnhay(11,3);
    while (1) { delay(1); }
  }

  finger.getTemplateCount();
  Serial.print("Sensor contains ");  Serial.print(finger.templateCount);  Serial.println(" templates");
  Serial.println("Waiting for valid finger...");
}

uint8_t getFingerprintID() {
  uint8_t p = finger.getImage();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image taken");
      Serial.println(p);
      break;
    case FINGERPRINT_NOFINGER:
      Serial.println("\nNo finger detected");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_IMAGEFAIL:
      Serial.println("Imaging error");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK success!
  p = finger.image2Tz();
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return p;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return p;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return p;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Could not find fingerprint features");
      return p;
    default:
      Serial.println("Unknown error");
      return p;
  }

  // OK converted!
  p = finger.fingerFastSearch();
  if (p == FINGERPRINT_OK) {
    onLed(G);
    Serial.println("Found a print match!");
  }
  else if (p == FINGERPRINT_PACKETRECIEVEERR) {
    Serial.println("Communication error");
    return p;
  }
  else if (p == FINGERPRINT_NOTFOUND) {
    OnOff(R);
    Serial.println("Did not find a match");
    return p;
  }
  else {
    OnOff(R);
    Serial.println("Unknown error");
    return p;
  }

  // found a match!
  Serial.print("Found ID #");
  Serial.print(finger.fingerID);
  sendFigerprintToServer(finger.fingerID)
  offLed(G);
  return finger.fingerID;
}

void loop()
{
  getFingerprintID();

  delay(50);
}