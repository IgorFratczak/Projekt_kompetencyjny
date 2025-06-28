"""
Funkcja generująca strukture pliku index.html

date - data rozpoczęcia zbierania danych
report_data_json - string zawierający dane z pliku more_info.json
"""
def generate_index_html(date: str = "", report_data_json: str = "{}"):
    header = f'''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Dane {date}</title>
        '''

    style = '''    
    <style>
            body { padding: 0; margin: 0; font-size: 20px; font-family: 'Inter', sans-serif; background-color: #dedede; }
            .wrapper { width: 100vw; height: auto; position: relative; }
            .left-menu { float: left; width: 20%; height: auto; background-color: #fff; position: relative; box-shadow: 0 8px 10px -6px rgb(137, 137, 149, 1); padding: 30px 0; margin-left: 5%; margin-top: 50px; }
            .left-menu-header { width: 90%; float: left; margin-left: 10%; color: #3c6fb2; }
            .left-menu-item { width: 80%; float: left; font-size: 0.85rem; margin: 5px 0 5px 20%; }
            .left-menu-item > a { text-decoration: none; color: #6098e0; transition: 0.3s; }
            .left-menu-item:hover > a { text-decoration: underline; color: #3c6fb2; }
            .right-container { float: right; width: 60%; height: auto; margin: 25px 7.5% 50px; }
            .right-container-item { width: 100%; height: auto; background-color: #fff; box-shadow: 0 8px 10px -6px rgb(137, 137, 149, 1); position: relative; padding: 30px 0; margin: 25px 0; float: left; }
            .right-container-item-header { width: 90%; padding-left: 5%; font-size: 1.8rem; margin-bottom: 20px; color: #3c6fb2; }
            .right-container-item-body { width: 90%; height: auto; margin-left: 5%; }
            .right-container-item-body > img { width: 100%; }
            .timestamp-header { width: 90%; margin-left: 7%; font-size: 1.3rem; color: #595959; margin-bottom: 40px; }
            .timestamp-body { width: 95%; margin-left: 2.5%; position: relative; height: auto; }
            .timestamp-item { width: 20%; float: left; padding: 0 2.5%; }
            .timestamp-item-header { display: flex; align-items: center; justify-content: center; font-size: 1.1rem; text-align: center; color: #3c6fb2; }
            .timestamp-item-body { width: 90%; margin: 10px 5%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; color: #595959; text-align: center; }
            .blinking-body { width: 90%; margin-left: 5%; position: relative; }
            .blinking-body-item { margin: 20px 0; font-size: 1.15rem; padding-left: 5%; color: #595959; }
            .blinking-body-item-label { color: #3c6fb2; }
            .blinking-body-item.closed { padding-left: 10%; }
            .rotating-body { width: 90%; height: 60vh; min-height: 400px; margin-left: 5%; border: 3px solid rgb(137, 137, 149, 1); position: relative; display: grid; grid-template-columns: 1fr 2fr 1fr; grid-template-rows: 1fr 2fr 1fr; }
            .rotating-body > div { display: flex; justify-content: center; align-items: center; color: white; font-size: 1.8rem; font-weight: bold; background-color: #1a59a9; transition: opacity 0.5s ease-in-out; border-right: 3px solid rgb(137, 137, 149, 1); border-bottom: 3px solid rgb(137, 137, 149, 1); }
            .rotating-body > div:nth-child(3n) { border-right: none; }
            .rotating-body > div:nth-child(n+7) { border-bottom: none; }
        </style>
    </head>
    '''
    body_start = '''<body>
    <div class="wrapper">
        <div class="left-menu">
            <div class="left-menu-header">Dane ogólne:</div>
            <div class="left-menu-item"><a href="#timeStamps">• Czas symulacji i poszczególne przedziały czasowe</a></div>
            <div class="left-menu-item"><a href="#eyeBlinkingAndClosed">• Mruganie i zamknięcie oczu</a></div>
            <div class="left-menu-item"><a href="#eyeRotating">• Rotacja wzroku</a></div>
            <div class="left-menu-header">Wykresy:</div>
            <div class="left-menu-item"><a href="#leftEyeClosed">• Zamknięcie lewego oka</a></div>
            <div class="left-menu-item"><a href="#rightEyeClosed">• Zamknięcie prawego oka</a></div>
            <div class="left-menu-item"><a href="#leftCheekRise">• Uniesienie lewego policzka</a></div>
            <div class="left-menu-item"><a href="#rightCheekRise">• Uniesienie prawego policzka</a></div>
            <div class="left-menu-item"><a href="#leftSmile">• Uniesienie lewego kącika ust</a></div>
            <div class="left-menu-item"><a href="#rightSmile">• Uniesienie prawego kącika ust</a></div>
            <div class="left-menu-item"><a href="#leftLipDepressor">• Obniżenie lewego kącika ust</a></div>
            <div class="left-menu-item"><a href="#rightLipDepressor">• Obniżenie prawego kącika ust</a></div>
            <div class="left-menu-item"><a href="#leftDimpler">• Cofnięcie lewego kącika ust</a></div>
            <div class="left-menu-item"><a href="#rightDimpler">• Cofnięcie prawego kącika ust</a></div>
            <div class="left-menu-item"><a href="#leftLidTightner">• Zmrużenie lewego oka</a></div>
            <div class="left-menu-item"><a href="#rightLidTightner">• Zmrużenie prawego oka</a></div>
            <div class="left-menu-item"><a href="#leftLidRise">• Rozszerzenie lewego oka</a></div>
            <div class="left-menu-item"><a href="#rightLidRise">• Rozszerzenie prawego oka</a></div>
            <div class="left-menu-item"><a href="#leftBrowRise">• Uniesienie lewej brwi</a></div>
            <div class="left-menu-item"><a href="#rightBrowRise">• Uniesienie prawej brwi</a></div>
            <div class="left-menu-item"><a href="#leftBrowLower">• Obniżenie lewej brwi</a></div>
            <div class="left-menu-item"><a href="#rightBrowLower">• Obniżenie prawej brwi</a></div>
            <div class="left-menu-item"><a href="#jawDrop">• Obniżenie szczęki</a></div>
            <div class="left-menu-header">Emocje:</div>
            <div class="left-menu-item"><a href="#flight">• Cały lot</a></div>
            <div class="left-menu-item"><a href="#flightStart">• Procedura startu</a></div>
            <div class="left-menu-item"><a href="#flightNormal">• Spokojny lot</a></div>
            <div class="left-menu-item"><a href="#flightTurbulence">• Turbulencje</a></div>
            <div class="left-menu-item"><a href="#flightLanding">• Procedura londowania</a></div>
        </div>
        '''
    body_center = f'''<div class="right-container">
            <div class="right-container-item">
                <div class="right-container-item-header">Dane z dnia</div>
                <div class="timestamp-header">{date}</div>
            </div>
            '''

    body_bottom = f'''   <div id="timeStamps" class="right-container-item">
                <div class="right-container-item-header">Czas symulacji i poszczególne przedziały czasowe</div>
                <div class="timestamp-header">Ładowanie...</div>
                <div class="timestamp-body"></div>
            </div>
            <div id="eyeBlinkingAndClosed" class="right-container-item">
                <div class="right-container-item-header">Mruganie i zamknięcie oczu</div>
                <div class="blinking-body"><p>Ładowanie...</p></div>
            </div>
            <div id="eyeRotating" class="right-container-item">
                <div class="right-container-item-header">Rotacja wzroku</div>
                <div class="rotating-body">
                    <div class="upper_left"></div><div class="upper_center"></div><div class="upper_right"></div>
                    <div class="left"></div><div class="center"></div><div class="right"></div>
                    <div class="bottom_left"></div><div class="bottom_center"></div><div class="bottom_right"></div>
                </div>
            </div>
            <div id="leftEyeClosed" class="right-container-item"><div class="right-container-item-header">Wykres zamknięcia lewego oka</div><div class="right-container-item-body"><img src="./plots/left_eye_closed.png" alt="Brak wykresu zamknięcia lewego oka"></div></div>
            <div id="rightEyeClosed" class="right-container-item"><div class="right-container-item-header">Wykres zamknięcia prawego oka</div><div class="right-container-item-body"><img src="./plots/right_eye_closed.png" alt="Brak wykresu zamknięcia prawego oka"></div></div>
            <div id="leftCheekRise" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia lewego policzka</div><div class="right-container-item-body"><img src="./plots/left_cheek_rise.png" alt="Brak wykresu uniesienia lewego policzka"></div></div>
            <div id="rightCheekRise" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia prawego policzka</div><div class="right-container-item-body"><img src="./plots/right_cheek_rise.png" alt="Brak wykresu uniesienia prawego policzka"></div></div>
            <div id="leftSmile" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia lewego kącika ust</div><div class="right-container-item-body"><img src="./plots/left_smile.png" alt="Brak wykresu uniesienia lewego kącika ust"></div></div>
            <div id="rightSmile" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia prawego kącika ust</div><div class="right-container-item-body"><img src="./plots/right_smile.png" alt="Brak wykresu uniesienia prawego kącika ust"></div></div>
            <div id="leftLipDepressor" class="right-container-item"><div class="right-container-item-header">Wykres obniżenia lewego kącika ust</div><div class="right-container-item-body"><img src="./plots/left_lip_depressor.png" alt="Brak wykresu obniżenia lewego kącika ust"></div></div>
            <div id="rightLipDepressor" class="right-container-item"><div class="right-container-item-header">Wykres obniżenia prawego kącika ust</div><div class="right-container-item-body"><img src="./plots/right_lip_depressor.png" alt="Brak wykresu obniżenia prawego kącika ust"></div></div>
            <div id="leftDimpler" class="right-container-item"><div class="right-container-item-header">Wykres cofnięcia lewego kącika ust</div><div class="right-container-item-body"><img src="./plots/left_dimpler.png" alt="Brak wykresu cofnięcia lewego kącika ust"></div></div>
            <div id="rightDimpler" class="right-container-item"><div class="right-container-item-header">Wykres cofnięcia prawego kącika ust</div><div class="right-container-item-body"><img src="./plots/right_dimpler.png" alt="Brak wykresu cofnięcia prawego kącika ust"></div></div>
            <div id="leftLidTightner" class="right-container-item"><div class="right-container-item-header">Wykres zmrużenia lewego oka</div><div class="right-container-item-body"><img src="./plots/left_lid_tightner.png" alt="Brak wykresu zmrużenia lewego oka"></div></div>
            <div id="rightLidTightner" class="right-container-item"><div class="right-container-item-header">Wykres zmrużenia prawego oka</div><div class="right-container-item-body"><img src="./plots/right_lid_tightner.png" alt="Brak wykresu zmrużenia prawego oka"></div></div>
            <div id="leftLidRise" class="right-container-item"><div class="right-container-item-header">Wykres rozszerzenia lewego oka</div><div class="right-container-item-body"><img src="./plots/left_lid_riser.png" alt="Brak wykresu rozszerzenia lewego oka"></div></div>
            <div id="rightLidRise" class="right-container-item"><div class="right-container-item-header">Wykres rozszerzenia prawego oka</div><div class="right-container-item-body"><img src="./plots/right_lid_riser.png" alt="Brak wykresu rozszerzenia prawego oka"></div></div>
            <div id="leftBrowRise" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia lewej brwi</div><div class="right-container-item-body"><img src="./plots/left_inner_brow_rise.png" alt="Brak wykresu uniesienia lewej brwi"></div></div>
            <div id="rightBrowRise" class="right-container-item"><div class="right-container-item-header">Wykres uniesienia prawej brwi</div><div class="right-container-item-body"><img src="./plots/right_inner_brow_rise.png" alt="Brak wykresu uniesienia prawej brwi"></div></div>
            <div id="leftBrowLower" class="right-container-item"><div class="right-container-item-header">Wykres obniżenia lewej brwi</div><div class="right-container-item-body"><img src="./plots/left_brow_lower.png" alt="Brak wykresu obniżenia lewej brwi"></div></div>
            <div id="rightBrowLower" class="right-container-item"><div class="right-container-item-header">Wykres obniżenia prawej brwi</div><div class="right-container-item-body"><img src="./plots/right_brow_lower.png" alt="Brak wykresu obniżenia prawej brwi"></div></div>
            <div id="jawDrop" class="right-container-item"><div class="right-container-item-header">Wykres obniżenia szczęki</div><div class="right-container-item-body"><img src="./plots/jaw_drop.png" alt="Brak wykresu obniżenia szczęki"></div></div>
            <div id="flight" class="right-container-item"><div class="right-container-item-header">Wykres emocji podczas całego lotu</div><div class="right-container-item-body"><img src="./plots/flight.png" alt="Brak wykresu emocji podczas całego lotu"></div></div>
            <div id="flightStart" class="right-container-item"><div class="right-container-item-header">Wykres emocji podczas procedury startu</div><div class="right-container-item-body"><img src="./plots/flight_start.png" alt="Brak wykresu emocji podczas procedury startu"></div></div>
            <div id="flightNormal" class="right-container-item"><div class="right-container-item-header">Wykres emocji podczas spokojnego lotu</div><div class="right-container-item-body"><img src="./plots/flight_normal.png" alt="Brak wykresu emocji podczas spokojnego lotu"></div></div>
            <div id="flightTurbulence" class="right-container-item"><div class="right-container-item-header">Wykres emocji podczas turbulencji</div><div class="right-container-item-body"><img src="./plots/flight_turbulence.png" alt="Brak wykresu emocji podczas turbulencji"></div></div>
            <div id="flightLanding" class="right-container-item"><div class="right-container-item-header">Wykres emocji podczas procedury lądowania</div><div class="right-container-item-body"><img src="./plots/flight_landing.png" alt="Brak wykresu emocji podczas procedury lądowania"></div></div>
        </div>
    </div>
    <script>
        const reportData = {report_data_json};
    </script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            try {{
                if (reportData && Object.keys(reportData).length > 0) {{
                    populateTimeStamps(reportData.time);
                    populateEyeData(reportData.eye);
                    populateEyesRotationData(reportData.eyes_rotation);
                }} else {{
                    throw new Error("Dane raportu (reportData) są puste lub nie istnieją.");
                }}
            }} catch (error) {{
                console.error("Nie udało się przetworzyć danych raportu:", error);
                document.querySelector('#timeStamps .timestamp-header').textContent = "Błąd wczytywania danych.";
                document.querySelector('#eyeBlinkingAndClosed .blinking-body').innerHTML = "<p>Błąd wczytywania danych.</p>";
            }}
            function populateTimeStamps(timeData) {{
                if (!timeData) return;
                const durationHeader = document.querySelector('#timeStamps .timestamp-header');
                const timeStampsBody = document.querySelector('#timeStamps .timestamp-body');
                timeStampsBody.innerHTML = '';
                durationHeader.textContent = `Czas symulacji: ${{timeData.duration}} s`;
                const phaseMap = {{ start: 'Procedura startu', normal: 'Spokojny lot', turbulence: 'Turbulencje', landing: 'Procedura lądowania' }};
                for (const key in phaseMap) {{
                    const phaseTitle = phaseMap[key];
                    const totalDuration = timeData[`${{key}}_duration`];
                    const intervals = timeData[key];
                    const phaseItemDiv = document.createElement('div');
                    phaseItemDiv.className = 'timestamp-item';
                    phaseItemDiv.innerHTML = `<div class="timestamp-item-header">${{phaseTitle}}<br>(${{totalDuration}} s)</div>`;
                    if (intervals && intervals.length > 0) {{
                        intervals.forEach(interval => {{
                            const intervalBodyDiv = document.createElement('div');
                            intervalBodyDiv.className = 'timestamp-item-body';
                            intervalBodyDiv.innerHTML = `${{interval.start}} s - ${{interval.end}} s<br>(${{interval.duration}} s)`;
                            phaseItemDiv.appendChild(intervalBodyDiv);
                        }});
                    }} else {{
                        phaseItemDiv.innerHTML += `<div class="timestamp-item-body">Brak danych</div>`;
                    }}
                    timeStampsBody.appendChild(phaseItemDiv);
                }}
            }}
            function populateEyeData(eyeData) {{
                if (!eyeData) {{ console.error("Brak danych 'eye' w pliku JSON."); return; }}
                const blinkingBody = document.querySelector('#eyeBlinkingAndClosed .blinking-body');
                if (!blinkingBody) {{ console.error("Nie znaleziono kontenera '#eyeBlinkingAndClosed .blinking-body'"); return; }}
                const longestClosure = eyeData.closed_eyes.time_stamps.reduce((max, current) => current.duration > max ? current.duration : max, 0);
                let closedTimeStampsHTML = '';
                if (eyeData.closed_eyes.time_stamps.length > 0) {{
                    eyeData.closed_eyes.time_stamps.forEach(ts => {{
                        closedTimeStampsHTML += `<div class="blinking-body-item closed">${{ts.start}} s - ${{ts.end}} s (${{ts.duration}} s)</div>`;
                    }});
                }} else {{
                    closedTimeStampsHTML = `<div class="blinking-body-item closed">Brak zdarzeń.</div>`;
                }}
                blinkingBody.innerHTML = `
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia:</span> ${{eyeData.blinking.count}}</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia podczas całej symulacji:</span> ${{eyeData.blinking.mean}} (mrugnięcia / min)</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia podczas procedury startu:</span> ${{eyeData.blinking.mean_per_minute_start}} (mrugnięcia / min)</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia podczas spokojnego lotu:</span> ${{eyeData.blinking.mean_per_minute_normal}} (mrugnięcia / min)</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia podczas turbulencji:</span> ${{eyeData.blinking.mean_per_minute_turbulence}} (mrugnięcia / min)</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Mrugnięcia podczas procedury lądowania:</span> ${{eyeData.blinking.mean_per_minute_landing}} (mrugnięcia / min)</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Zamknięcia oczu podczas całej symulacji:</span> ${{eyeData.closed_eyes.count}}</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Najdłuższe zamknięcie oczu:</span> ${{longestClosure.toFixed(3)}} s</div>
                    <div class="blinking-body-item"><span class="blinking-body-item-label">Zamknięcia oczu:</span></div>
                    ${{closedTimeStampsHTML}}`;
            }}
            function populateEyesRotationData(rotationData) {{
                if (!rotationData) {{ console.error("Brak danych 'eyes_rotation' w pliku JSON."); return; }}
                const gridMap = {{ upper_left: ".upper_left", upper_center: ".upper_center", upper_right: ".upper_right", left: ".left", center: ".center", right: ".right", bottom_left: ".bottom_left", bottom_center: ".bottom_center", bottom_right: ".bottom_right" }};
                const gridContainer = document.querySelector('#eyeRotating .rotating-body');
                for (const key in gridMap) {{
                    const selector = gridMap[key];
                    const cell = gridContainer.querySelector(selector);
                    if (cell) {{
                        const percentage = rotationData[key];
                        cell.textContent = `${{percentage}}%`;
                    }}
                }}
            }}
        }})
    </script>
    </body>
</html>
    '''

    return header + style + body_start + body_center + body_bottom