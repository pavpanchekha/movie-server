<section>
<h1 title="Playlists">Playlists</h1>
%for playlist in playlists:
  <div class="item XXX">
      <form method="post" action="/playlist/{{playlist['id']}}">
        <button name="action" value="start">
          <img class="start" src="/static/start.png" height="48px" alt="Play" />
        </button>
    </div>
    <div class="rightcol">
      <h2>{{playlist['title']}}</h2>
    </div>
  </div>
%end for
<div class="item XXX">
  <div class="leftcol">
    <form method="post" action="/playlist/*">
      <button name="action" value="start">
        <img class="start" src="/static/start.png" height="48px" alt="Play" />
      </button>
    </form>
  </div>
  <div class="rightcol">
    <h2>All Music</h2>
  </div>
</div>
</section>
