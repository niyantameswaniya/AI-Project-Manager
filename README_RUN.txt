============================================
  AI Project Manager - Run karne ke tareeke
============================================

OPTION 1 - Sirf backend (sabse simple)
--------------------------------------
1. run-backend-only.bat double-click karo
2. Browser mein kholo: http://127.0.0.1:8000
   - API docs: http://127.0.0.1:8000/docs
   - Agar frontend build hai to full app dikhega

OPTION 2 - Full app (backend + frontend)
--------------------------------------
1. Pehle build-frontend.bat chalao (sirf ek baar)
2. Phir run.bat chalao
3. Browser: http://127.0.0.1:8000

OPTION 3 - run.bat (build try karega, phir backend)
--------------------------------------------------
1. run.bat double-click karo
2. Build fail ho to bhi backend start hoga
3. http://127.0.0.1:8000 kholo (docs to milega hi)

--------------------------------------------
Agar "python is not recognized" aaye:
  -> Python install karo, "Add to PATH" tick karo
  -> https://www.python.org/downloads/

Agar "npm is not recognized" aaye:
  -> Node.js install karo
  -> https://nodejs.org/

Agar backend start ho jaye par browser mein kuch nahi:
  -> Pehle run build-frontend.bat, phir run.bat
============================================
