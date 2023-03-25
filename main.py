from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

videoPutArgs = reqparse.RequestParser()
videoPutArgs.add_argument("name", type=str, help="Name of the video is required", required=True)
videoPutArgs.add_argument("views", type=int, help="Views of the video is required", required=True)
videoPutArgs.add_argument("likes", type=int, help="Likes of the video is required", required=True)

videos = {}

def AbortIfVideoIdDoesntExist(videoId):
    if videoId not in videos:
        abort(404, message="Could not find video...")

class Video(Resource):
    def get(self, videoId):
        abort(videoId)
        return videos[videoId]
    
    def put(self, videoId):
        args = videoPutArgs.parse_args()
        videos[videoId] = args
        return videos[videoId], 201

    
api.add_resource(Video, "/video/<int:videoId>")

if __name__ == "__main__":
    app.run(debug=True)