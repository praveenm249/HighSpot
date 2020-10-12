Scale requirements: Apply changes when mixtape.json and/or changes.json are too large to fit in memory

I would do stream processing of the json file using generators in python with start and end parameters for the chunk,
stream processing of json is a bit tricky as the object can split into multiple lines at each level.
It would be much easier if each object is on single line like json-lines format then we can use pandas library to stream.
So without json-lines we have to gracefully parse the objects by writing a custom parser using regex and identify the end
and get the next chunk from there. The parser will return a valid json. Once we get the chunk we can load into memory
and then we should check if the chunk has the playlists that we are interested in i.e add, remove and update.
For remove we just remove the node, for add we need to check if we have reached the end of playlists to add the playlist
there will be few edge cases for this, for update we need to check if the song exists but the songs may not be in the
current chunk so we update the playlist without any checks but keep track of chunk, paylist id and song id so that
we can update back at the end if the song does not exist. we can store all the processed chunks seperately until we
finish processing and combine them at the end.

If the changes file is also large,  I would do a preprocess of the changes file and get it to a format in ascending order
like {id1 :{remove:id1, add:{}, update:{}},
      id2 :{remove:id2, add:{}, update:{}}}
and do a stream processing of changes and as we process through mixtape.json we can do all the changes for an id, once all
the id's are processed in the changes chunk then we can get next chunk.

Key part of above approach is stream processing and parsing the chunks gracefully. This approach would be slower than loading
the whole file into memory but it will get the job done.
