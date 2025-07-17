#include <Arduino.h>
#include <U8x8lib.h>
U8X8_SSD1306_128X64_ALT0_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);
int minLight = 20;
int maxLight = 100;
int lightVal = 0;
void setup(void) {
  u8x8.begin();
  u8x8.setFlipMode(1);
  Serial.begin(9600);

}
void loop(void) {
  lightVal = analogRead(A6);
  Serial.print(lightVal);
  u8x8.setFont(u8x8_font_chroma48medium8_r);
  u8x8.setCursor(0, 0);
  u8x8.print("Light: ");
  u8x8.print(lightVal);
  u8x8.setCursor(0, 33);
  if (lightVal < minLight){
    u8x8.println("too dark!!");
  }else if (lightVal > maxLight){
    u8x8.println("too bright!!");
  } else {
    u8x8.println("IDEAL :D");}
  delay(300);
} 