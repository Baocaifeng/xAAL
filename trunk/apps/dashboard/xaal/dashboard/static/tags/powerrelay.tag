<powerrelay>

<div class="powerrelay">
<div class="{stateClass}">{ power }</div>
  <button class="button ripple" name="btn_on" onclick={ btn }>ON</button>
  <button class="button ripple" name="btn_off" onclick={ btn }>OFF</button>
</div>

<script>
  this.addr = opts.xaal_addr
  this.power = '__';
  this.stateClass = 'state-unknow';

  receive(data) {
    state = data['attributes']['power']
    if (state == true) {
      this.power = 'ON'
      this.stateClass = 'state-on'
    }
    else {
      this.power = 'OFF'
      this.stateClass = 'state-off'
    }
    this.update()
 }

  btn(e) {
    if (e.target.name =='btn_on')
      sio_send_request(this.addr,'on',{})
    if (e.target.name =='btn_off')
      sio_send_request(this.addr,'off',{})
  }
</script>

<style>
 .powerrelay {
 }

 .state-on {
     color:  var(--color3);
     font-weight: bold;
     padding: 8px;
 }

 .state-unknow, .state-off {
     color:  var(--color1);
     font-weight: bold;
     padding: 8px;
 }

</style>
</powerrelay>
