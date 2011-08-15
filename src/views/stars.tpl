%if rating is not None:
  %for i in range(rating):
    <img src="/static/heart.png" alt="*" />
  %end for
  %for i in range(rating, 5):
    <img src="/static/noheart.png" alt="." />
  %end for
%end if
