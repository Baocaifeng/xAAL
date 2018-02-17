<%inherit file="base.mako"/>



<h2>Information</h2>
<table width=100%>
  <tr><th>Addr</th><th>devtype</th><th>Info</th><th>Attributes</th></tr>
  % for dev in devs:  
  <tr>
    <td><a href="/generic/${dev.address}">${dev.address}</a></td>
    <td>${dev.devtype}</td>
    %if 'info' in dev.description.keys():
       <td>${dev.description['info']}</td>
    %else:
       <td>--</td>
    %endif
    %if 'embedded' in dev.attributes.keys():
        <td>embedded</td>
    %else:
        <td>${dev.attributes}</td>
    %endif
  </tr>
  % endfor
</table>

