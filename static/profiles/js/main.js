
function toggleOnlineList() {
    var onlineLists = document.querySelectorAll('.online-list');
    // Loop through each online list and toggle its visibility
    onlineLists.forEach(function (list) {
        list.classList.toggle('hidden');
    });
    var linkText = document.getElementById('hideConversationLink').innerText;
    if (linkText === 'Hide Chat') {
        document.getElementById('hideConversationLink').innerText = 'Show Chat';
    } else {
        document.getElementById('hideConversationLink').innerText = 'Hide Chat';
    }
}
function closeModal() {
    var nameModal = document.getElementById('nameModal');
    nameModal.style.display = 'none';
}
function toggleMoreInfo(event) {
    // Prevent the default link behavior
    event.preventDefault();

    // Find the parent event container
    var eventContainer = event.target.closest('.event');

    // Find the more-info section within the event container
    var moreInfoSection = eventContainer.querySelector('.more-info');

    // Toggle the visibility of the more-info section
    moreInfoSection.classList.toggle('hidden');
}


var storedValues = {
    region: "",
    name: "",
    BIO: "",
    email: "",
    contact: "",
    bankID: "",
    frameSize: "",
    onlinePaymentInput: "",
    Image: "",
    ExpectedIncome: "",
    Skill: ""

};
function toggleUpdateOptions() {
    var updateOptionsDiv = document.getElementById('updateOptions');
    var leftSidebarContent = document.querySelector('.imp-links');
    if (updateOptionsDiv.style.display === 'none') {
        updateOptionsDiv.classList.add('move-upward-animation'); //added for css
        // Hide other left sidebar content
        leftSidebarContent.style.display = 'none';
        // Move update options to the top of the left sidebar
        document.getElementById('leftSidebar').insertAdjacentElement('afterbegin', updateOptionsDiv);
        // Show update options
        updateOptionsDiv.style.display = 'block';
        // Store current values in variables when update options are shown
        storedValues.region = document.getElementById('regionInput').value;
        storedValues.name = document.getElementById('nameInput').value;
        storedValues.email = document.getElementById('emailInput').value;
        storedValues.contact = document.getElementById('contactInput').value;
        storedValues.Image = document.getElementById('profilePic').value;


    } else {
        leftSidebarContent.style.display = 'block';
        updateOptionsDiv.style.display = 'none';
        updateOptionsDiv.classList.add('move-upward-animation');
        // Move update options back to its original position
        document.getElementById('leftSidebar').appendChild(updateOptionsDiv);
        // Revert input fields to stored values when update options are hidden
        document.getElementById('regionInput').value = storedValues.region;
        document.getElementById('nameInput').value = storedValues.name;
        document.getElementById('emailInput').value = storedValues.email;
        document.getElementById('contactInput').value = storedValues.contact;
        document.getElementById('profilePic').value = storedValues.Image;

    }
}
function cancelChanges() {
    toggleUpdateOptions();
    document.getElementById('regionInput').value = storedValues.region;
    document.getElementById('nameInput').value = storedValues.name;
    document.getElementById('emailInput').value = storedValues.email;
    document.getElementById('contactInput').value = storedValues.contact;
    document.getElementById('profilePic').value = storedValues.Image;
}
function updateChanges() {
    var farmerID = document.getElementById('FarmerID').value;
    var newName = document.getElementById('nameInput').value;
    var region = document.getElementById('regionInput').value;
    var name = document.getElementById('nameInput').value;
    var BIO = document.getElementById('BIO').value;
    var email = document.getElementById('emailInput').value;
    var contact = document.getElementById('contactInput').value;
    var bankID = document.getElementById('bankIDInput').value;
    var frameSize = document.getElementById('frameSizeInput').value;
    var onlinePaymentInput = document.getElementById('onlinePaymentInput').value;

    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];

    formData.append('image', file);
    formData.append('farmerID', farmerID);
    formData.append('name', name);
    formData.append('BIO', BIO);
    formData.append('email', email);
    formData.append('region', region);
    formData.append('contact', contact);
    formData.append('bankID', bankID);
    formData.append('frameSize', frameSize);
    formData.append('onlinePaymentInput', onlinePaymentInput);

    var message = "Region: " + region + "\n";
    message += "Name: " + name + "\n";
    message += "BIO: " + BIO + "\n";
    message += "Email: " + email + "\n";
    message += "Contact: " + contact + "\n";
    message += "Bank ID: " + bankID + "\n";
    message += "Frame Size: " + frameSize + "\n";
    message += "Online Payment Number: " + onlinePaymentInput + "\n";
    message += "profilePic: " + fileInput + "\n";
    if (confirm("Your information has been updated:\n\n" + message + "\nDo you want to proceed with the upgrade?")) {
        // Send the data to the server using fetch or any other method
        fetch('/update_farmer', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => {
                console.log(result);
                // Handle the response from the server if needed
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors if any
            });

        storedValues.region = region;
        storedValues.name = name;
        storedValues.email = email;
        storedValues.Image = fileInput;
        document.getElementById('userName').innerText = name;
        toggleUpdateOptions();


        // Create a new FileReader object to read the uploaded image
        const reader = new FileReader();

        // Define a function to execute after the image has been read
        reader.onload = function (event) {
            // Get the URL of the uploaded image
            const imageUrl = event.target.result;

            // Update the src attribute of the profile image dynamically
            document.getElementById('profilePic').src = imageUrl;
        };

        // Read the uploaded image as a data URL
        reader.readAsDataURL(file);

    } else {
        cancelChanges();
    }
}



function updateChanges_admin() {
    var AdminID = document.getElementById('AdminID').value;
    var newName = document.getElementById('nameInput').value;
    var region = document.getElementById('regionInput').value;
    var name = document.getElementById('nameInput').value;
    var email = document.getElementById('emailInput').value;
    var contact = document.getElementById('contactInput').value;

    console.log("badmin" + AdminID)
    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    formData.append('image', file);
    formData.append('AdminID', AdminID);
    formData.append('name', name);
    formData.append('email', email);
    formData.append('region', region);
    formData.append('contact', contact);

    var message = "Region: " + region + "\n";
    message += "Name: " + name + "\n";
    message += "Email: " + email + "\n";
    message += "Contact: " + contact + "\n";
    message += "profilePic: " + fileInput + "\n";
    if (confirm("Your information has been updated:\n\n" + message + "\nDo you want to proceed with the upgrade?")) {
        // Send the data to the server using fetch or any other method
        fetch('/update_Admin', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => {
                console.log(result);
                // Handle the response from the server if needed
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors if any
            });

        storedValues.region = region;
        storedValues.name = name;
        storedValues.email = email;
        storedValues.contact = contact;
        storedValues.Image = fileInput;

        document.getElementById('userName').innerText = name;
        toggleUpdateOptions();

        const reader = new FileReader();

        // Define a function to execute after the image has been read
        reader.onload = function (event) {
            // Get the URL of the uploaded image
            const imageUrl = event.target.result;

            // Update the src attribute of the profile image dynamically
            document.getElementById('profilePic').src = imageUrl;
        };

        // Read the uploaded image as a data URL
        reader.readAsDataURL(file);
    } else {
        cancelChanges();
    }
}


function updateChanges_Laborer() {
    var LaborerID = document.getElementById('LaborerID').value;
    var region = document.getElementById('regionInput').value;
    var name = document.getElementById('nameInput').value;
    var email = document.getElementById('emailInput').value;

    var Skill = document.getElementById('Skill').value;
    var ExpectedIncome = document.getElementById('ExpectedIncome').value;
    var OnlinePaymentNumber = document.getElementById('OnlinePaymentNumber').value;
    var Bankid = document.getElementById('bankIDInput').value;
    var contact = document.getElementById('contactInput').value;

    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    formData.append('image', file);
    formData.append('LaborerID', LaborerID);
    formData.append('name', name);
    formData.append('email', email);
    formData.append('region', region);
    formData.append('Skill', Skill);
    formData.append('ExpectedIncome', ExpectedIncome);
    formData.append('OnlinePaymentNumber', OnlinePaymentNumber);
    formData.append('Bankid', Bankid);
    formData.append('contact', contact);

    var message = "Region: " + region + "\n";
    message += "Name: " + name + "\n";
    message += "Email: " + email + "\n";
    message += "Contact: " + contact + "\n";
    message += "profilePic: " + fileInput + "\n";
    if (confirm("Your information has been updated:\n\n" + message + "\nDo you want to proceed with the upgrade?")) {
        // Send the data to the server using fetch or any other method
        fetch('/update_Laborer', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => {
                console.log(result);
                // Handle the response from the server if needed
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors if any
            });

        storedValues.region = region;
        storedValues.name = name;
        storedValues.email = email;
        storedValues.contact = contact;
        storedValues.Image = fileInput;
        document.getElementById('userName').innerText = name;
        toggleUpdateOptions();

        const reader = new FileReader();

        // Define a function to execute after the image has been read
        reader.onload = function (event) {
            // Get the URL of the uploaded image
            const imageUrl = event.target.result;

            // Update the src attribute of the profile image dynamically
            document.getElementById('profilePic').src = imageUrl;
        };

        // Read the uploaded image as a data URL
        reader.readAsDataURL(file);
    } else {
        cancelChanges();
    }
}




function updateChanges_Buyer() {
    var BuyerID = document.getElementById('BuyerID').value;
    var UserID = document.getElementById('UserID').value;
    var region = document.getElementById('regionInput').value;
    var name = document.getElementById('nameInput').value;
    var email = document.getElementById('emailInput').value;
    
    var OnlinePaymentNumber = document.getElementById('OnlinePaymentNumber').value;
    var Bankid = document.getElementById('bankIDInput').value;
    var contact = document.getElementById('contactInput').value;

    console.log(UserID)
    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    formData.append('image', file);
    formData.append('UserID', UserID);
    formData.append('name', name);
    formData.append('email', email);
    formData.append('region', region);
    formData.append('OnlinePaymentNumber', OnlinePaymentNumber);
    formData.append('Bankid', Bankid);
    formData.append('contact', contact);

    var message = "Region: " + region + "\n";
    message += "Name: " + name + "\n";
    message += "Email: " + email + "\n";
    message += "Contact: " + contact + "\n";
    message += "profilePic: " + fileInput + "\n";
    if (confirm("Your information has been updated:\n\n" + message + "\nDo you want to proceed with the upgrade?")) {
        // Send the data to the server using fetch or any other method
        fetch('/update_Buyerr', {
            method: 'POST',
            body: formData
        })
            .then(response => response.text())
            .then(result => {
                console.log(result);
                // Handle the response from the server if needed
            })
            .catch(error => {
                console.error('Error:', error);
                // Handle errors if any
            });

        storedValues.region = region;
        storedValues.name = name;
        storedValues.email = email;
        storedValues.contact = contact;
        storedValues.Image = fileInput;
        document.getElementById('userName').innerText = name;
        toggleUpdateOptions();

        const reader = new FileReader();

        // Define a function to execute after the image has been read
        reader.onload = function (event) {
            // Get the URL of the uploaded image
            const imageUrl = event.target.result;

            // Update the src attribute of the profile image dynamically
            document.getElementById('profilePic').src = imageUrl;
        };

        // Read the uploaded image as a data URL
        reader.readAsDataURL(file);
    } else {
        cancelChanges();
    }
}



document.getElementById("signoutBtn").addEventListener("click", function () {
    if (confirm("Are you sure you want to sign out?")) {
        window.location.href = "signout.html";
    }
});

document.getElementById('searchInput').addEventListener('keypress', function (e) {

    var Ques = document.getElementById('searchInput').value;
    console.log(Ques);
    if (e.key === 'Enter' && Ques !== "") {
        console.log("Hello")
        search();
    } else if (e.key === 'Enter' && Ques == "") {
        $('#search-results').empty();
        $('#tableContainer').hide();
        console.log("in else");
    }
});


// Function to handle adding a user and changing button text
function addUser(userid) {
    // Send AJAX request to Flask backend to start conversation
    var userId = document.getElementById('UserID').value;
    console.log("Sender " + userId)
    $.ajax({
        url: '/start_conversation',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ sender_id: userId, receiver_id: userid }),
        success: function (response) {
            console.log("Conversation started!");
            // Change button text to "Added"
            $(`#addBtn_${userId}`).text("Added");
            // Disable the button after it's clicked
            $(`#addBtn_${userId}`).prop('disabled', true);
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });

}

// Function to handle search and display results
function search() {
    var Ques = document.getElementById('searchInput').value;

    // Send AJAX request to Flask backend using jQuery
    $.ajax({
        url: '/search',
        type: 'POST',
        data: { Ques: Ques },
        success: function (response) {
            // Clear previous search results
            $('#search-results').empty();

            // Parse the JSON response
            var Result = JSON.parse(response);
            console.log(Result);
            // Iterate through each laborer and append HTML to the search results area
            Result.forEach(function (result) {
                console.log(result);
                var html = `
        
        <tr>
            <td>${result.id}</td>
            <td>${result.username}</td>
            <td>
                <button id="addBtn_${result.id}" class="btn" onclick="addUser(${result.id})">
                    Add
                </button>
            </td>
            <td>
                <button class="btn">
                   View 
                </button>
            </td>
        </tr>
    
        `;
                $('#search-results').append(html);
            });

            // Show the table after populating search results
            $('#tableContainer').show();

        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });
}



function search_friend() {
    var Ques = document.getElementById('UserID').value;

    // Send AJAX request to Flask backend using jQuery
    $.ajax({
        url: '/index',
        type: 'POST',
        data: { Ques: Ques },
        success: function (response) {
            // Clear previous search results
            $('#search-results').empty();

            // Parse the JSON response
            var Result = JSON.parse(response);
            console.log(Result);
            // Iterate through each laborer and append HTML to the search results area
            Result.forEach(function (result) {
                console.log(result);
                var html = `
        
        <tr>
            <td>${result.id}</td>
            <td>${result.username}</td>
            <td>
                <button class="btn">
                    Remove
                </button>
            </td>
            <td>
                <button class="btn">
                   View 
                </button>
            </td>
        </tr>
    
        `;
                $('#search-results').append(html);
            });

            // Show the table after populating search results
            $('#tableContainer').show();
        },
        error: function (xhr, status, error) {
            console.error('Error:', error);
        }
    });
}


function toggleDropdown() {
    var dropdownContent = document.getElementById("dropdownContent");

    if (dropdownContent.style.display === "block") {
        dropdownContent.style.display = "none";
    } else {
        dropdownContent.style.display = "block";
    }
}

document.getElementById("dropdown-icon").addEventListener("click", toggleDropdown);

document.getElementById("userName").addEventListener("click", toggleDropdown);



