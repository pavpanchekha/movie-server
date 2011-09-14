%def head():
    <link rel="stylesheet" href="/static/library.css" />
    <script src="/static/library.js"></script>
    <script src="/static/touchswipe.js"></script>
%end

%rebase master title="Library", head=head

<div id="all">
%include libplaylists playlists=playlists
%include libmovies movies=movies
</div>
