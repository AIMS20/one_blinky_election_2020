int datafromUser=0;
const int DEMS = 12;
const int REPS = 13;

const int bluePin   = 6;     
const int greenPin  = 5;        
const int redPin    = 3;

void setup() {
  // put your setup code here, to run once:
  Serial.flush();
  pinMode( DEMS , OUTPUT );
  pinMode( REPS , OUTPUT );
  pinMode( bluePin , OUTPUT );
  pinMode( greenPin , OUTPUT );
  pinMode( redPin , OUTPUT );

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0)
  {
    datafromUser=Serial.read();
  }

  if(datafromUser == 'b')
  {
    voteToggle(DEMS);
  }
  if(datafromUser == 'r')
  {
    voteToggle(REPS);
  }
  else if(datafromUser == 's')
  {
    digitalWrite( DEMS , HIGH );
    digitalWrite( REPS , HIGH );
  }
   if(datafromUser == 'x')
  {
    voteToggle(REPS);
    voteToggle(DEMS);

  }
  if(datafromUser == 'c')
  {
    RGB_change();
  }
  if(datafromUser == 'B')
  {
    RGB_BIDEN();
  }
  else if(datafromUser == 'T')
  {
    RGB_TRUMP();
  }
  if(datafromUser == '1')
  {
    RGB_full(0, 0, 255);
  }
  else if(datafromUser == '2')
  {
    RGB_full(255, 0, 0);
  }
}

void voteToggle(int PIN){

    digitalWrite( PIN , LOW );
    delay(100);
    digitalWrite( PIN , HIGH );
    delay(100);
    digitalWrite( PIN , LOW );
    delay(100);
    digitalWrite( PIN , HIGH );
  }

void RGB_full(int red, int green, int blue){
    analogWrite(redPin, red);     
    analogWrite(greenPin,green);     
    analogWrite(bluePin, blue);
    Serial.flush();

  }
  
void RGB_change(){
    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, 0);
    delay(100);

  for(int i=0; i<10;i++){
      analogWrite(redPin, 255);
      delay(300);
      analogWrite(redPin, 0);
      analogWrite(greenPin, 255);
      delay(300);
      analogWrite(greenPin, 0);
      analogWrite(bluePin, 255);
      delay(300);
      analogWrite(bluePin, 0);
  }
    Serial.flush();

}

 
void RGB_BIDEN(){
  RGB_change();
    delay(100);
    digitalWrite(12, LOW);
    digitalWrite(13, LOW);

    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    while(true){
      analogWrite(bluePin, 255);
      delay(300);
      analogWrite(bluePin, 0);
      delay(300);
     }
  }


 void RGB_TRUMP(){
  RGB_change();
    delay(100);
    digitalWrite(12, LOW);
    digitalWrite(13, LOW);

    analogWrite(bluePin, 0);
    while(true){
      analogWrite(redPin, 255);
      analogWrite(greenPin, 255);
      delay(300);
      analogWrite(redPin, 0);
      analogWrite(greenPin, 0);
      delay(300);
     }
  }
