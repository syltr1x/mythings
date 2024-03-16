void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "ON") {
      digitalWrite(13, HIGH);
    } else if (command == "OFF") {
      digitalWrite(13, LOW);
    }
  }
}
