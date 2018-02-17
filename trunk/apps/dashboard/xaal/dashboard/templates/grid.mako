<%inherit file="base.mako"/>
<%namespace name="devices" file="device_def.mako" />

<div class="grid-background">
<div class="grid">

   <div class="grid-box">
    <div style="text-align:center;">
      <b>Eclairage Entrée</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da03"></span>
      <b>Eclairage Couloir</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da05"></span>
    </div>
  </div>

  <div class="grid-box">
    <div style="text-align:center;">
      <b>Eclairage salon</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da08"></span>
      <b>Eclairage salle</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da07"></span>
    </div>
  </div>

    
  <div class="grid-box">
    <div style="text-align:center;">
      <b>Eclairage Cuisine</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da04"></span>
      <b>Eclairage SDB</b>
      <span data-is="lamp" xaal_addr="ccc44227-d4fc-46eb-8578-159e2c47da06"></span>
    </div>
  </div>
    


 <div class="grid-box">
  <div style="text-align:center;">
    <b>Wall Plug</b>
    <span data-is="powerrelay" xaal_addr="0aebfee4-04f6-11e8-8a43-00fec8f7138c"></span>
    <br/>
    <span data-is="powermeter" xaal_addr="0aebfee4-04f6-11e8-8a43-00fec8f7138d"></span>
  </div>
 </div>


 <div class="grid-box">
  <div style="text-align:center;">
    <b>Test2</b>
    ${devices.thermometer("c1c955a1-8bd3-4c37-b31c-047da2bbd3fa")}
  </div>
 </div>


 

  <div class="grid-box">
    <div>
      <b>Température</b>  <i class="fa fa-thermometer-half temperature" aria-hidden="true"></i>
        <table>
          <tr>
            <td>Extérieur</td>
            <td>
              <a href="/generic/c1c955a1-8bd3-4c37-b31c-047da2bbd3fa">
                <span data-is="thermometer" xaal_addr="c1c955a1-8bd3-4c37-b31c-047da2bbd3fa"></span>
              </a>
            </td>
          </tr>
          <tr>
            <td>Bureau</td>
            <td>
              <a href="/generic/b4cec9fa-7513-4d87-bfc1-ee1107176cf0">
                <span data-is="thermometer" xaal_addr="b4cec9fa-7513-4d87-bfc1-ee1107176cf0"></span>
              </a>
            </td>
          </tr>

          <tr>
            <td>Salon</td>
            <td>
              <a href="/generic/2f31c921-01b2-4097-bfae-5753dde2cd42">
                <span data-is="thermometer" xaal_addr="2f31c921-01b2-4097-bfae-5753dde2cd42"></span>
              </a>
            </td>
          </tr>

          <tr>
            <td>Ch1</td>
            <td>
              <a href="/generic/2f31c933-01b2-4097-bfae-5753dde2cd42">
                <span data-is="thermometer" xaal_addr="2f31c933-01b2-4097-bfae-5753dde2cd42"></span>
              </a>
            </td>
          </tr>

          <tr>
            <td>Ch2</td>
            <td>
              <a href="/generic/2f31c933-01b2-4097-bfae-5753dde2cd42">
                <span data-is="thermometer" xaal_addr="2f31c933-01b2-4097-bfae-5753dde2cd42"></span>
              </a>
            </td>
          </tr>




        </table>
    </div>
  </div>


  <div class="grid-box">
    <div>
      <b>Humidité</b>
        <table>
          <tr>
            <td>Exterieur</td>
            <td>
              <a href="/generic/c1c955a2-8bd3-4c37-b31c-047da2bbd3fa">
                <span data-is="hygrometer" xaal_addr="c1c955a2-8bd3-4c37-b31c-047da2bbd3fa"></span>
              </a>
            </td>
          </tr>

          <tr>
            <td>Bureau</td>
            <td>
              <a href="/generic/b4cec9fa-7513-4d87-bfc1-ee1107176cf1">
                <span data-is="hygrometer" xaal_addr="b4cec9fa-7513-4d87-bfc1-ee1107176cf1"></span>
              </a>
            </td>
          </tr>


          <tr>
            <td>Salon</td>
            <td>
              <a href="/generic/2f31c921-01b2-4097-bfae-5753dde2cd43">
                <span data-is="hygrometer" xaal_addr="2f31c921-01b2-4097-bfae-5753dde2cd43"></span>
              </a>
            </td>
          </tr>




        </table>
    </div>
  </div>




  <div class="grid-box two">
    <div data-is="generic-attrs" xaal_addr="8b71f050-b334-11e7-bca7-00fec8f7138c"></div>
  </div>

  <div class="grid-box two" style="align:center;">
    	<!-- img src="http://10.77.3.51/video3.mjpg" width=250 -->
  </div>

  <div class="grid-box" style="text-align:center;">
    <br/><br/><br/>
      <span data-is="clock"/>
  </div>

  
  <div class="grid-box">
      <div>
        <b>EDF</b><br/>
        O kW
      </div>
  </div>



  
  <div class="grid-box">Foo</div>
</div> <!-- end of grid -->
</div><!-- end of grib background -->

<script type="riot/tag" src="/static/tags/powerrelay.tag"></script>
<script type="riot/tag" src="/static/tags/hygrometer.tag"></script>
<script type="riot/tag" src="/static/tags/thermometer.tag"></script>
<script type="riot/tag" src="/static/tags/powermeter.tag"></script>
<script type="riot/tag" src="/static/tags/lamp.tag"></script>


<script type="riot/tag" src="/static/tags/generic_attrs.tag"></script>
<script type="riot/tag" src="/static/tags/clock.tag"></script>
