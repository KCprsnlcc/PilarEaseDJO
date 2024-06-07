
        document.querySelectorAll('.v1_124 div').forEach(item => {
            item.addEventListener('click', function() {
                // Remove 'active' class from all spans
                document.querySelectorAll('.v1_127, .v1_129, .v1_131, .v1_133, .v1_135, .v1_137, .v1_139, .v1_141').forEach(span => {
                    span.classList.remove('active');
                });
                // Add 'active' class to clicked span
                this.querySelector('span').classList.add('active');
            });
        });
    
        // Check for click events on the "EXPRESS YOUR FEELINGS" button
        document.getElementById('loginButton').addEventListener('click', function() {
            console.log('Login button clicked'); // Debugging statement
            document.getElementById('dialogOverlay').style.display = 'block';
            document.getElementById('dialogBox').style.display = 'block';
        });
    
        // Check for click events on the close button
        document.getElementById('dialogClose').addEventListener('click', function() {
            console.log('Close button clicked'); // Debugging statement
            document.getElementById('dialogOverlay').style.display = 'none';
            document.getElementById('dialogBox').style.display = 'none';
        });
    
        // Hide the modal if the user clicks outside of it
        window.onclick = function(event) {
            var modal = document.getElementById('dialogBox');
            if (event.target == modal) {
                modal.style.display = 'none';
                document.getElementById('dialogOverlay').style.display = 'none';
            }
        };
    
        // Randomize curves
        document.querySelectorAll('.curved-line path').forEach(function(path) {
            var controlPointX1 = Math.random() * 50; // Random control point X1
            var controlPointY1 = Math.random() * 50; // Random control point Y1
            var controlPointX2 = 100 - Math.random() * 50; // Random control point X2
            var controlPointY2 = Math.random() * 50; // Random control point Y2
            var endPointX = Math.random() * 100; // Random end point X
            var endPointY = Math.random() * 100; // Random end point Y
            var d = `M0,0 C${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${endPointX},${endPointY}`; // Construct path data
            path.setAttribute('d', d); // Set path data
        });