// firebase-config.js
// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-app.js";
import { getFirestore, doc, getDoc, setDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.13.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDLY7ie39rKxvU_Evkq-VK25uvlVgqm6yQ",
  authDomain: "diesesi-spiel-ist-gesund.firebaseapp.com",
  databaseURL: "https://diesesi-spiel-ist-gesund-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "diesesi-spiel-ist-gesund",
  storageBucket: "diesesi-spiel-ist-gesund.appspot.com",
  messagingSenderId: "419197734080",
  appId: "1:419197734080:web:834d4e0854eed5cec53125"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);

export { db, doc, getDoc, setDoc, deleteDoc };
