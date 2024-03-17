#include "WiFi.h"
#include "esp_camera.h"
#include "Arduino.h"
#include "soc/soc.h"           
#include "soc/rtc_cntl_reg.h"  
#include "driver/rtc_io.h"
#include <FS.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>

//Enter your network credentials
const char* ssid = "YRZPhone";
const char* password = "#Jaihind20";

#define API_KEY "AIzaSyDKzdFq44XLPspZEsfLBWtfmzQYp9KB0jk"

// ENter Authorized Email and Password
#define USER_EMAIL "seenusanjay20102002@gmail.com"
#define USER_PASSWORD "#Jaihind20"

// Enter Firebase storage bucket ID
#define STORAGE_BUCKET_ID "smart-surveillance-37cd5.appspot.com"

#define IMAGE_PATH "image.jpg"

// OV2640 camera module pins (CAMERA_MODEL_AI_THINKER)
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22


FirebaseData fbdo;
FirebaseAuth authentication;
FirebaseConfig configuration;


void setup() {
  Serial.begin(115200);

  pinMode(12,OUTPUT);
  digitalWrite(12,HIGH);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

 // initialize OV2640 camera module
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0; 
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    ESP.restart();
  } 

  configuration.api_key = API_KEY;
  authentication.user.email = USER_EMAIL;
  authentication.user.password = USER_PASSWORD;
  configuration.token_status_callback = tokenStatusCallback; 

  Firebase.begin(&configuration, &authentication);
  Firebase.reconnectWiFi(true);
}

void loop() {

  camera_fb_t * fb = NULL; 
  Serial.println("ESP32-CAM capturing photo...");

  fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Failed");
    return;
  }
  
  uint8_t* frame_data = new uint8_t[fb->len];
  memcpy(frame_data, fb->buf, fb->len);

  if (Firebase.ready())
  {
      Serial.print("Uploading Photo... ");
  
     if (Firebase.Storage.upload(&fbdo, STORAGE_BUCKET_ID, frame_data, fb->len, IMAGE_PATH, "image/jpg" ))
      {
        Serial.printf("\nDownload URL: %s\n", fbdo.downloadURL().c_str());
      }
      
      else
      {
        Serial.println(fbdo.errorReason());
      }
    }
    else 
    {
      Serial.println("Firebase not ready");
    }

    esp_camera_fb_return(fb);
    delete[] frame_data;
}
