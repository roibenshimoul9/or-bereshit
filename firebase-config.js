// Firebase web config for Or Bereshit.
// These values identify the Firebase project and are public by design; access to data is
// protected by the Firestore security rules (firestore.rules) and the authorized domains list.
// Paste the object from Firebase console → Project settings → Your apps → Web app → Config.
window.FIREBASE_CONFIG = {
  apiKey: "AIzaSyC3Xxi4zQdAoHuZfQylztcHWoQmu8bVukw",
  authDomain: "or-bereshit.firebaseapp.com",
  projectId: "or-bereshit",
  storageBucket: "or-bereshit.firebasestorage.app",
  messagingSenderId: "1012143534685",
  appId: "1:1012143534685:web:d7cf307c305998c4b8d3b4"
};

// Accounts that see the admin page (#/admin). Keep in sync with isAdmin() in firestore.rules.
window.OB_ADMIN_EMAILS = ['roibenshimoul9@gmail.com'];
