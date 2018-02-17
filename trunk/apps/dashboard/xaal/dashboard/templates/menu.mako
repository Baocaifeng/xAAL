  <!-- Menu -->
  <ul class="menu">
    <li><a href="#" onclick="openNav()">&#9776;</a></li>     
% for item in menu.get():
  %  if item.has_key('active'):
    <li class="active"><a href="${item['url']}">${item['value']}</a></li>
  %  else:
    <li><a href="${item['url']}">${item['value']}</a></li>
  % endif
% endfor
  </ul>
  <!-- EOF Menu -->
