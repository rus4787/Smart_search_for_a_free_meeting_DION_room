// client/room-search.js

function searchRooms() {
    const time = document.getElementById("time").value;

    // Имитируем отправку запроса на сервер для поиска комнаты
    fetch('http://localhost:5003/search_room', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "time": time })
    })
    .then(response => response.json())
    .then(data => {
        const roomResults = document.getElementById("room-results");
        roomResults.innerHTML = '';

        if (data.rooms && data.rooms.length > 0) {
            data.rooms.forEach(room => {
                const roomElement = document.createElement("div");
                roomElement.innerText = `Room ID: ${room.room_id} is available at ${time}`;
                roomResults.appendChild(roomElement);
            });
        } else {
            roomResults.innerText = 'No available rooms at the selected time.';
        }
    })
    .catch(error => console.error('Error:', error));
}
