%def head():
    <link rel="stylesheet" href="/static/library.css" />
    <script src="/static/library.js"></script>
%end

%rebase master title="Library", head=head

<h1>Playlists</h1>
%for playlist in playlists:
  <div class="item">
    <div class="leftcol">
      <form method="post" action="/">
        <input type="hidden" name="file" value="playlist:{{playlist['id']}}" />
        <button name="action" value="start">
          <img class="start" src="/static/start.png" height="48px" alt="Play" />
        </button>
      </form>
    </div>
    <div class="rightcol">
      <h2>{{playlist['title']}}</h2>
    </div>
  </div>
%end for
<div class="item">
  <div class="leftcol">
    <form method="post" action="/">
      <input type="hidden" name="file" value="playlist:*" />
      <button name="action" value="start">
        <img class="start" src="/static/start.png" height="48px" alt="Play" />
      </button>
    </form>
  </div>
  <div class="rightcol">
    <h2>All Music</h2>
  </div>
</div>
