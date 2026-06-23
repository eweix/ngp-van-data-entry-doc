1. MyVoters
2. Canvass Results
3. Contact Type: `Walk`
4. Date To/From if desired

```javascript
{
  const myWards = `Dane - City Of Madison - Ward 058
Dane - City Of Madison - Ward 059
Dane - City Of Madison - Ward 060
Dane - City Of Madison - Ward 061
Dane - City Of Madison - Ward 062
Dane - City Of Madison - Ward 063
Dane - City Of Madison - Ward 064
Dane - City Of Madison - Ward 065
Dane - City Of Madison - Ward 066
Dane - City Of Madison - Ward 067
Dane - City Of Madison - Ward 069
Dane - City Of Madison - Ward 070
Dane - City Of Madison - Ward 071
Dane - City Of Madison - Ward 080
Dane - City Of Madison - Ward 085
Dane - City Of Madison - Ward 086
Dane - City Of Madison - Ward 087
Dane - City Of Madison - Ward 088
Dane - City Of Madison - Ward 089
Dane - City Of Madison - Ward 090
Dane - City Of Madison - Ward 091
Dane - City Of Madison - Ward 092
Dane - City Of Madison - Ward 093
Dane - City Of Madison - Ward 094
Dane - City Of Madison - Ward 096
Dane - City Of Madison - Ward 109
Dane - City Of Madison - Ward 110
Dane - City Of Madison - Ward 111
Dane - City Of Madison - Ward 112
Dane - City Of Madison - Ward 113
Dane - City Of Madison - Ward 114
Dane - City Of Madison - Ward 115
Dane - City Of Madison - Ward 116
Dane - City Of Madison - Ward 117
Dane - City Of Madison - Ward 118
Dane - City Of Madison - Ward 119
Dane - City Of Madison - Ward 134
Dane - City Of Middleton - Ward 001
Dane - City Of Middleton - Ward 002
Dane - City Of Middleton - Ward 003
Dane - City Of Middleton - Ward 004
Dane - City Of Middleton - Ward 005
Dane - City Of Middleton - Ward 006
Dane - City Of Middleton - Ward 007
Dane - City Of Middleton - Ward 008
Dane - City Of Middleton - Ward 009
Dane - City Of Middleton - Ward 010
Dane - City Of Middleton - Ward 011
Dane - City Of Middleton - Ward 012
Dane - City Of Middleton - Ward 013
Dane - City Of Middleton - Ward 014
Dane - City Of Middleton - Ward 015
Dane - City Of Middleton - Ward 016
Dane - City Of Middleton - Ward 017
Dane - City Of Middleton - Ward 018
Dane - City Of Middleton - Ward 019
Dane - City Of Middleton - Ward 021
Dane - City Of Middleton - Ward 022
Dane - City Of Middleton - Ward 024
Dane - Town Of Middleton - Ward 001
Dane - Town Of Middleton - Ward 002
Dane - Town Of Middleton - Ward 003
Dane - Town Of Middleton - Ward 004
Dane - Town Of Middleton - Ward 004a
Dane - Town Of Middleton - Ward 005
Dane - Town Of Middleton - Ward 006
Dane - Town Of Middleton - Ward 007
Dane - Town Of Middleton - Ward 008
Dane - Town Of Middleton - Ward 008a
Dane - Village Of Shorewood Hills - Ward 001
Dane - Village Of Shorewood Hills - Ward 002`
    .split('\n')
    .map(w => w.trim())
    .filter(Boolean);

  const wardSet = new Set(myWards.map(w => w.toLowerCase()));

  const table = document.getElementById('ctl00_ContentPlaceHolderVANPage_gvList');
  const rows = Array.from(table.querySelectorAll('tr')).slice(1);

  let grandTotal = 0;
  const matched = [];
  const matchedNames = new Set();

  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    if (cells.length === 0) return;

    const wardName = cells[0].textContent.trim();
    if (!wardSet.has(wardName.toLowerCase())) return;

    const lastCell = cells[cells.length - 1];
    const total = parseInt(lastCell.textContent.trim(), 10) || 0;

    matched.push({ ward: wardName, total });
    matchedNames.add(wardName.toLowerCase());
    grandTotal += total;
  });

  console.table(matched);
  console.log(`TOTAL DOORS ATTEMPTED ACROSS ${matched.length} OF ${myWards.length} WARDS ON YOUR LIST: ${grandTotal}`);

  const missing = myWards.filter(w => !matchedNames.has(w.toLowerCase()));
  if (missing.length) {
    console.warn(`Not found on this page (${missing.length}):`, missing);
  }
}

```
