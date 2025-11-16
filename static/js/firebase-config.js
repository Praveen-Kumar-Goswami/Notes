const firebaseConfig = {
    apiKey: "AIzaSyBhevkc0Foxzxxhd9RyUM5B254F9-b0rec",
    authDomain: "my-med-app-c7880.firebaseapp.com",
    databaseURL: "https://my-med-app-c7880-default-rtdb.asia-southeast1.firebasedatabase.app",
    projectId: "my-med-app-c7880",
    storageBucket: "my-med-app-c7880.firebasestorage.app",
    messagingSenderId: "1074750455581",
    appId: "1:1074750455581:web:c22edd4d0454cd4c32abf4",
    measurementId: "G-82NG41VYHN"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

