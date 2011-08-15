<div id="controls">
  <form method="post" action="/hegemony" id="hegemony">
    <ul>
    %for host, description in hosts.items():
      %if heg[host]:
        <li><input type="checkbox" checked="yes" name="server" value="{{host}}" id="server:{{host}}" /><label for="server:{{host}}">{{description}}</label></li>
      %else:
        <li><input type="checkbox" name="server" value="{{host}}" id="server:{{host}}" /><label for="server:{{host}}">{{description}}</label></li>
      %end if
    %end for
    </ul>
  </form>
  <form method="post" action="/{{mod}}/{{name}}">
    <button id="popup" name="action" value="hegemony"><img src="/static/outputs.png" height="48px" alt="Outputs" /></button>
    <button name="action" value="stop"><img src="/static/stop.png" height="48px" alt="Stop" /></button>
    %if is_playing:
      <button name="action" value="pause"><img src="/static/pause.png" height="48px" alt="Pause" /></button>
    %else:
      <button name="action" value="play"><img src="/static/start.png" height="48px" alt="Play" /></button>
    %end if
  </form>
</div>
