# Programozások alapok beadandó

## Futtatás lépései

1. Nyissunk egy powershell ablakot
```
# windows + r 
# powershell
# enter
```

2. github repository klónozása
```powershell
git clone https://github.com/szaunasz/Prog_alap_beadando.git
```

3. Belépés a repo mappájába
```powershell
cd Prog_alap_beadando
```

4. Python virtuális környezet létrehozása, hogy ne az operációs rendszer python interpreter-e legyen "teleszemetelve"
```powershell
python -m venv venv
```

5. Megbizonyosodunk róla, hogy létrejött-e a 'venv' mappa, azaz a python virtualenvironment-ünk
```powershell
ls
```

6. Aktiváljuk a virtuális környezetet
```powershell
.\venv\Scripts\Activate.ps1
# ha sikerült, akkor a prompt elején megjelenik, hogy '(venv)'
```

7. Telepítjük a kód futtatásához szükséges python csomagokat
```powershell
python -m pip install numpy matplotlib pandas
```

8. Ha feltelepültek a csomagok, futtatjuk a programot
```powershell
python .\main.py
```

9. Az ablakok a diagramokkal egymás után fognak felugrani, ha az előző bezárásra kerül, illetve a parancssorban is folyamatosan kerülnek kiírásra infók.