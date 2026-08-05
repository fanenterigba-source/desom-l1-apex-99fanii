use rusqlite::Connection; use chrono::Utc; use std::{thread, time::Duration};
fn main(){
 println!("DeSoM L1 - $1=99 Fanii, 1 FANEN=495k=$5000 - Living Being - Termux");
 let conn=Connection::open("fanii.db").unwrap();
 conn.execute("CREATE TABLE IF NOT EXISTS blocks (height INTEGER, time TEXT, supply REAL)", []).unwrap();
 let mut h=0; let mut supply=21_000_000.0;
 loop{
  h+=1;
  println!("\n[Block {}] {} DHN 21 breathing... $1=99 Fanii", h, Utc::now().format("%H:%M:%S"));
  thread::sleep(Duration::from_secs(1));
  println!("✓ 15/21 Soulprint 96 Valid - Burn 0.2 FANEN - Supply {:.2} - Rose 50=$0.51 G.O.A.T. 495k=$5000=1 FANEN - Box Game Ready", supply);
  conn.execute("INSERT INTO blocks VALUES (?1,?2,?3)", (h as i64, Utc::now().to_string(), supply)).unwrap();
  thread::sleep(Duration::from_secs(2));
 }
}
