%def head():
    <link rel="stylesheet" href="/static/library.css" />
    <script src="/static/library.js"></script>
    <script src="/static/touchswipe.js"></script>
%end

%rebase master title="Library", head=head

<section>
<h1 title="Movies">Movies</h1>
%for movie in movies:
  <div class="item">
    <div class="leftcol">
      <form method="post" action="/movie/{{movie['id']}}">
        <button name="action" value="start">
          <img class="start" src="/static/start.png" height="48px" alt="Play" />
          <img class="cover" src="{{movie['image']}}" width="100%" />
        </button>
      </form>
      <div class="rating">
      %include stars rating=movie["rating"]
      </div>
    </div>
    <div class="rightcol">
      <h2>{{movie['title']}}</h2>
      <p class="summary hyphenate">{{movie['description']}} <span class="duration">{{movie['duration']}}</span></p>
    </div>
  </div>
%end for
</section>
