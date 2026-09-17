// Firebase web config for Or Bereshit.
// These values identify the Firebase project and are public by design; access to data is
// protected by the Firestore security rules (firestore.rules) and the authorized domains list.
// Paste the object from Firebase console → Project settings → Your apps → Web app → Config.
window.FIREBASE_CONFIG = null;
/* example:
window.FIREBASE_CONFIG = {
  apiKey: "...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "...",
  appId: "..."
};
*/

// Accounts that see the admin page (#/admin). Keep in sync with isAdmin() in firestore.rules.
window.OB_ADMIN_EMAILS = ['roibenshimoul9@gmail.com'];
