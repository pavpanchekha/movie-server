$def with (item, is_playing, hosts, heg)
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf8">
    <meta name="viewport" content="width=device-width; height=device-height; initial-scale=1.0; user-scalable=0;" />
    <title>$item['title']</title>
    <link rel="stylesheet" href="/static/main.css" />
    <link rel="stylesheet" href="/static/playlist.css" />
    <link rel="apple-touch-icon-precomposed" href="/static/icon.png" />
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
    <script src="/static/main.js"></script>
    <script src="/static/controls.js"></script>
    <script src="/static/playlist.js"></script>
  </head>
  <body>
    <h1>$item["title"]</h1>
    <form method="post" action="/">
      <input type="hidden" name="action" value="skip" />
      <ol start="$item['position']">
      $for id, song in item["songs"]:
        $if id + 1 == item["position"]:
          <li id="song$id" class="active"><button class="song" name="position" value="$id">$song</button></li>
        $else:
          <li id="song$id"><button class="song" name="position" value="$id">$song</button></li>
      </ol>
    </form>
    <div id="controls">
      <form method="post" action="/">
        <ul id="hegemony">
        $for host, description in hosts.items():
          $if heg[host]:
            <li><input type="checkbox" checked="yes" name="server" value="$host" id="server:$host" /><label for="server:$host">$description</label></li>
          $else:
            <li><input type="checkbox" name="server" value="$host" id="server:$host" /><label for="server:$host">$description</label></li>
        </ul>
        <button id="popup" name="action" value="hegemony"><img src="/static/outputs.png" height="48px" alt="Outputs" /></button>
        <button name="action" value="stop"><img src="/static/stop.png" height="48px" alt="Stop" /></button>
        $if is_playing:
          <button name="action" value="pause"><img src="/static/pause.png" height="48px" alt="Pause" /></button>
        $else:
          <button name="action" value="play"><img src="/static/start.png" height="48px" alt="Play" /></button>
      </form>
    </div>
  </body>
</html>
