// src/types/window.d.ts
// Extend the Window interface to include SpeechRecognition

interface Window {
  SpeechRecognition: any;
  webkitSpeechRecognition: any;
}

// Also declare these globally if needed
declare var SpeechRecognition: any;
declare var webkitSpeechRecognition: any;