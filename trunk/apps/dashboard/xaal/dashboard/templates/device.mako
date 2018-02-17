<%inherit file="base.mako"/>

<h1>Device ${dev.address}</h1>
<h2>${dev.devtype}</h2>


<div data-is="${data_is}" xaal_addr="${dev.address}" value="${value}"></div>
<script type="riot/tag" src="/static/tags/thermometer.tag"></script>
<script type="riot/tag" src="/static/tags/hygrometer.tag"></script>
<script type="riot/tag" src="/static/tags/powerrelay.tag"></script>
