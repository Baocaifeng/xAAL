<powermeter>

<span class="powermeter">
  <span class="power">{ power }&nbsp;W</span>
</span>


<script>
  this.addr = opts.xaal_addr;
  this.power = '__';
  receive(data) {
    this.power = data['attributes']['power'];
    this.update();
  }
</script>

<style>
. {
    font-weight: bold;
    color : var(--color1);
    align: center;
}
</style>

</powermeter>
