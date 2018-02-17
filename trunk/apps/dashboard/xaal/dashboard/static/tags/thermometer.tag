<thermometer>

<span class="thermometer">
    <span class="temperature">{ temperature }&nbsp;°</span>
</span>

<script>
  this.addr = opts.xaal_addr
  this.temperature = '__._';
  receive(data) {
    this.temperature = data['attributes']['temperature']
    this.update()
  }
</script>

<style>

.temperature {
    font-weight: bold;
    color : var(--color1);
}

.thermometer {
    padding: 10px 0px;
}

</style>


</thermometer>
