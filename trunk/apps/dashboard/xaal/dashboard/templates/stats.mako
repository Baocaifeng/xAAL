<%inherit file="base.mako"/>


<div class="content">

  <h1>Devices stats</h1>
  <div>Uptime: <b>${uptime}</b></div>
  <div>Total found devices : <b>${total}</b></div><br/>
  <table>
    <tr><th>Devtypes</th><th>counter</th></tr>
    % for dt in devtypes:
    <tr><td>${dt}</td><td>${devtypes[dt]}</td></tr>
    % endfor
    </table>
</div>
