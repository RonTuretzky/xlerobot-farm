"""Render the itemized companion to sensing slide 7 from the same price snapshot."""
import html
import json
from pathlib import Path


def build(here):
    data = json.loads((here / "sensor-bom.json").read_text())
    groups = {"basic": "Basic measurements", "chemistry": "Optional pH + conductivity", "optional": "Other optional measurements"}
    content = []
    for group, title in groups.items():
        selected = [item for item in data["items"].values() if item["group"] == group]
        total = sum(round(item["price"] * 100) for item in selected) / 100
        rows = ''.join(f'<tr><td><a href="{item["url"]}" target="_blank" rel="noopener noreferrer">{html.escape(item["name"])}</a></td><td>1 pack</td><td>${item["price"]:.2f}</td></tr>' for item in selected)
        content.append(f'<h2>{title}</h2><table><thead><tr><th>Amazon product</th><th>Order quantity</th><th>Pack price</th></tr></thead><tbody>{rows}</tbody></table><p>Group subtotal: <b>${total:.2f}</b></p>')
    basic = sum(round(i['price'] * 100) for i in data['items'].values() if i['group'] == 'basic') / 100
    chemistry = sum(round(i['price'] * 100) for i in data['items'].values() if i['group'] == 'chemistry') / 100
    doc = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Farm sensing parts — Amazon checklist</title>
<style>body{{background:#0b1513;color:#e6eee9;font:17px/1.6 system-ui,sans-serif;max-width:1050px;margin:auto;padding:40px 24px}}a{{color:#d7eafa;text-underline-offset:3px}}h1{{font-size:36px;line-height:1.15}}h2{{margin-top:40px;font-size:24px}}table{{width:100%;border-collapse:collapse}}td,th{{text-align:left;border-bottom:1px solid #54635c;padding:12px 8px}}td:last-child{{white-space:nowrap}}.note{{color:#bdc9c2;font-size:14px}}li{{margin:12px 0}}@media print{{body{{background:white;color:black}}a{{color:black}}}}</style>
<a href="xlerobot-deck.html#7">← Back to slide 7</a><h1>Farm sensing parts</h1>
<p><b>Basic: ${basic:.2f}. Basic + chemistry: ${basic + chemistry:.2f}.</b> Other optional measurements are extra; there is no need to buy them all.</p>
<p class="note">Amazon.com prices checked {data['checked']}, with Brooklyn 11222 displayed. One retail pack per line, before tax and shipping, without coupons. Prices and delivery can change. These are product links, not an order or a saved cart.</p>
{''.join(content)}
<h2>What is included, and what needs building</h2><ul>
<li>Use one ESP32, one HX711/load cell, one water probe, one air sensor and one light sensor. Extra units in multipacks are spares. The Mac and powered hub are already owned. Firmware and mechanical fixtures are still to be built.</li>
<li>Print the load-cell base and top plate, wrist holders and probe docks. The fastener pack covers a range of threads; confirm the actual load-cell threads before finalizing CAD. Calibrate with several weights across the expected pod mass, including the plate tare.</li>
<li>The DS18B20 pack includes adapter boards, wires and pull-up resistors. The breadboard kit includes male/male, male/female and female/female jumpers. Some breakout headers may need soldering. Tools and solder are excluded.</li>
<li>Use 3.3 V sensor logic and check each breakout's pinout. For the analog probes, one ADS1115 supplies multiple channels. The EC board can output 3.4 V: use a 1:1 divider made from two 10 kΩ resistors before a 3.3 V ADC, restore the factor of two in software, and calibrate. Do not connect a 5 V signal to the ESP32.</li>
<li>Both DFRobot pH and EC kits include a probe, signal board, cable and calibration solutions. Dip the probes separately and rinse between pods. Store the pH electrode in KCl. The DI-water price is an Amazon pack reference; sourcing rinse water locally can cost less.</li>
<li>The dissolved-oxygen kit does not include its required 0.5M NaOH electrolyte. It also needs the shared ADC and water-temperature sensor. Source this corrosive liquid locally in Japan and follow the manufacturer's handling instructions; protective equipment is excluded. This is deferred for the short microgreen trial.</li>
<li>The SCD41 measures CO₂, temperature and humidity, not airflow. It can replace the basic SHT31 if desired (subtract $9.99). The BT-816B is a handheld manual check, with a listed lower airspeed limit of 0.3 m/s; it cannot prove adequate gentle airflow around seedlings. The battery pack is a spare allowance.</li>
<li>BH1750 measures lux; AS7341 provides spectral channels. Neither is a calibrated PAR/PPFD instrument. A photo reference card does not measure daily light exposure. Photograph leaf area with known-size tags, and weigh harvested shoots separately: total wet-pot mass is not biomass.</li>
<li>Leak pads belong in a catch tray, powered briefly for readings to reduce corrosion. They need protection against splashes on exposed electronics. Cameras show symptoms, not definitive disease diagnoses; verify available servo telemetry on the actual kit.</li>
</ul>
<p class="note">Excludes robot, printer, filament, tools, protective equipment and local setup supplies. Nothing is installed in every pod.</p>
<h2>Manufacturer references</h2><p><a href="https://www.dfrobot.com/product-1782.html">pH kit contents and limits</a> · <a href="https://www.dfrobot.com/product-1123.html">EC output voltage, calibration and temperature compensation</a> · <a href="https://www.dfrobot.com/product-1628.html">Dissolved oxygen and electrolyte requirements</a> · <a href="https://device.report/m/66baf31afc2148a50e4dc362c643b7f05ed6793fb1986dcd10e2b38573188bbb">BTMETER manual</a></p></html>'''
    (here / 'sensor-shopping.html').write_text(doc)


if __name__ == '__main__':
    build(Path(__file__).parent)
