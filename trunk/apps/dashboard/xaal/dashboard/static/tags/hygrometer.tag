<hygrometer>

<span class="hygrometer">
  <span class="humidity">{ humidity }&nbsp;%</span>
</span>


<script>
  this.addr = opts.xaal_addr;
  this.humidity = '__';
  receive(data) {
    this.humidity = data['attributes']['humidity'];
    this.update();
  }
</script>


<style>
.humidity {
    font-weight: bold;
    color : var(--color1);
    align: center;
}
</style>

</hygrometer>
