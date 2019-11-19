const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();
const server = express();
server.use(cors());
server.use(express.json());

const token = process.env.MY_KEY;
const lambdaurl = 'https://lambda-treasure-hunt.herokuapp.com/api/adv';

function getExits(room) {
  return room.exits;
}

async function init() {
  return axios({
    url: `${lambdaurl}/init/`,
    method: 'GET',
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then(res => {
      // console.log(res.data);
      return res.data;
    })
    .catch(res => {
      console.log(res.data);
    });
}

async function move(dir) {
  return axios({
    url: `${lambdaurl}/move/`,
    method: 'POST',
    headers: {
      Authorization: `Token ${token}`,
      'Content-Type': 'application/json'
    },
    data: {
      direction: `${dir}`
    }
  })
    .then(res => {
      console.log('\nWALKING...\n');
      return res.data;
    })
    .catch(res => {
      console.log(res.data);
    });
}

function oppDir(dir) {
  if (dir === 'n') return 's';
  if (dir === 's') return 'n';
  if (dir === 'e') return 'w';
  if (dir === 'w') return 'e';
}

async function mapTraverse() {
  let currentRoom = await init();
  // console.log(currentRoom);

  let graph = {};
  let lastRoomID = currentRoom.room_id;
  let currentRoomID = currentRoom.room_id;
  graph[currentRoomID] = {};

  let exits = getExits(currentRoom);
  exits.forEach(exit => {
    graph[currentRoomID][exit] = '?';
  });
  let stack = [];
  stack.push(lastRoomID);
  console.log(graph);
  let count = 0;

  console.log(graph.length);
  while (count < 490) {
    while (stack.length > 0) {
      currentRoomID = stack.pop();
      if (!currentRoomID in graph) {
        count++;
        lastRoomID = currentRoomID;
        currentRoomID = currentRoom.room_id;
        graph[currentRoomID] = {};
        exits.forEach(exit => {
          if (exit === oppDir(direction)) {
            graph[currentRoomID][exit] = lastRoomID;
          } else {
            graph[currentRoomID][exit] = '?';
          }
        });
        for (let nextDir in graph[currentRoomID]) {
          if (graph[currentRoomID][nextDir] === '?') {
            lastRoomID = currentRoomID;
            direction = nextDir;
            console.log(direction);
            let currentRoom = await move(direction);
            console.log(currentRoom);
            stack.push(currentRoom.room_id);
          }
        }
      } else {
        if (currentRoom.room_id !== lastRoomID) {
          graph[lastRoomID][direction] = currentRoom.room_id;
        }
        for (let nextDir in graph[currentRoomID]) {
          if (graph[currentRoomID][nextDir] === '?') {
            lastRoomID = currentRoomID;
            direction = nextDir;
            let currentRoom = await move(direction);
            stack.push(currentRoom.room_id);
          } else {
            stack.pop();
          }
        }
      }
    }

    if (graph.length < 500) {
      let qq = [];
      qq.push([currentRoom.room_id]);
      lastRoomID = currentRoom.room_id;
      let visited = new Set();
      let route = [];
      let lastDir = direction;

      while (qq.length > 0) {
        let path = qq.shift();
        let roomID = path[path.length - 1];
        if (!roomID in visited) {
          visited.add(roomID);
          if ('?' in graph[roomID].values()) {
            break;
          } else {
            for (let [key, value] of Object.entries(graph[roomID])) {
              lastRoom = path[path.length - 1];
              let new_path = [...path];
              new_path.push(value);
              qq.push(new_path);
            }
          }
        }
      }
      path.reverse();

      while (path.length > 1) {
        let cur_room = path.pop();
        for (dir in graph[cur_room]) {
          if (graph[cur_room][dir] == path[path.length - 1]) {
            route.push(dir);
          }
        }
      }
      route.forEach(async step => {
        lastRoomID = currentRoom.room_id;
        let currentRoom = await move(step);
      });
      stack.push(currentRoom.room_id);
    }
  }
}

mapTraverse();
