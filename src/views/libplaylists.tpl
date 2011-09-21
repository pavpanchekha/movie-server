<section>
<h1 title="Playlists">Playlists</h1>
%for playlist in playlists:
  <div class="item small">
    <form class="leftcol" method="post" action="/playlist/{{playlist['id']}}">
      <button name="action" value="start">
        <img class="start" src="/static/start.png" height="48px" alt="Play" />
      </button>
    </form>
    <h2 class="rightcol">{{playlist['title']}}</h2>
  </div>
%end for
<div class="item small">
  <form class="leftcol" method="post" action="/playlist/*">
    <button name="action" value="start">
      <img class="start" src="/static/start.png" height="48px" alt="Play" />
    </button>
  </form>
  <h2 class="rightcol">All Music</h2>
</div>
</section>
