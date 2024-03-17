#define LED 2

void setup() {
  // put your setup code here, to run once:
  Serial.begin(112500);
  pinMode(LED,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("runn..");
  digitalWrite(LED,HIGH);
  delay(1000);
  digitalWrite(LED,LOW);
  delay(1000); 
}
