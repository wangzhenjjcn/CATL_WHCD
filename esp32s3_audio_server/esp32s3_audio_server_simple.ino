#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>
#include <driver/i2s.h>

// WiFi配置
const char* ssid = "1500M";
const char* password = "23457890";

// 服务器配置
WiFiServer server(8080);
WiFiClient client;

// I2S麦克风配置 - ESP32S3 XIAO Sense引脚
#define I2S_WS 15      // Word Select (WS)
#define I2S_SD 13      // Serial Data (SD)
#define I2S_SCK 2      // Serial Clock (SCK)
#define I2S_PORT I2S_NUM_0
#define BUFFER_SIZE 512

// 音频缓冲区
int16_t audioBuffer[BUFFER_SIZE];
int audioBufferIndex = 0;

void setup() {
  Serial.begin(115200);
  
  // 初始化I2S麦克风
  initI2SMic();
  
  // 连接WiFi
  connectToWiFi();
  
  // 启动服务器
  server.begin();
  Serial.println("服务器已启动，端口: 8080");
}

void loop() {
  // 检查客户端连接
  if (!client || !client.connected()) {
    client = server.available();
    if (client) {
      Serial.println("客户端已连接");
    }
  }
  
  // 读取音频数据
  readAudioData();
  
  // 如果有客户端连接，发送数据
  if (client && client.connected()) {
    sendRawAudioData();
  }
  
  delay(10); // 短暂延迟
}

void initI2SMic() {
  // I2S配置 - 针对ESP32S3优化
  const i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = (i2s_comm_format_t)(I2S_COMM_FORMAT_STAND_I2S),
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 1024,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  
  // I2S引脚配置
  const i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };
  
  // 初始化I2S
  esp_err_t err = i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  if (err != ESP_OK) {
    Serial.printf("I2S驱动安装失败: %s\n", esp_err_to_name(err));
    return;
  }
  
  err = i2s_set_pin(I2S_PORT, &pin_config);
  if (err != ESP_OK) {
    Serial.printf("I2S引脚设置失败: %s\n", esp_err_to_name(err));
    return;
  }
  
  err = i2s_start(I2S_PORT);
  if (err != ESP_OK) {
    Serial.printf("I2S启动失败: %s\n", esp_err_to_name(err));
    return;
  }
  
  Serial.println("I2S麦克风初始化完成");
}

void connectToWiFi() {
  Serial.print("连接到WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi连接成功!");
    Serial.print("IP地址: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("");
    Serial.println("WiFi连接失败!");
  }
}

void readAudioData() {
  size_t bytesRead = 0;
  esp_err_t err = i2s_read(I2S_PORT, &audioBuffer[audioBufferIndex], sizeof(int16_t), &bytesRead, 100);
  
  if (err == ESP_OK && bytesRead > 0) {
    audioBufferIndex++;
    
    // 当缓冲区满时，准备发送数据
    if (audioBufferIndex >= BUFFER_SIZE) {
      audioBufferIndex = 0;
    }
  }
}

// 发送原始音频数据
void sendRawAudioData() {
  if (client && client.connected()) {
    for (int i = 0; i < BUFFER_SIZE; i++) {
      client.print(audioBuffer[i]);
      if (i < BUFFER_SIZE - 1) {
        client.print(",");
      }
    }
    client.println();
    client.flush();
  }
} 