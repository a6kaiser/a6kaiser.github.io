function toggleSidebar() {
    var content = document.getElementById("content");
    var sidebarHeader = document.querySelector(".toggle-btn");
    var contentButton = document.getElementById("toggleButtonContent");

    content.classList.toggle("expanded"); // Expand/collapse the content area

    // Hide the sidebar button when content is expanded
    if (content.classList.contains("expanded")) {
        sidebarHeader.style.display = 'none'; // Hide the sidebar button

        // Delay the appearance of the content button until the animation is complete
        setTimeout(function() {
            contentButton.style.display = 'flex'; // Show content button after delay
        }, 300); // 300ms matches the animation duration
    } else {
        // Hide the content button and show the sidebar button
        contentButton.style.display = 'none'; // Hide content button
        sidebarHeader.style.display = 'flex'; // Show the sidebar button
    }
}

function scrollToSection(event, sectionId) {
        event.preventDefault(); // Prevent the default anchor behavior

        var section = document.getElementById(sectionId);
        var content = document.getElementById("content");
        var header = document.querySelector(".header");

        // Get the height of the header
        var headerHeight = header.offsetHeight;

        // Calculate the position of the section relative to the content div
        var sectionPosition = section.getBoundingClientRect().top + content.scrollTop;

        // Scroll to the section position minus the header height
        content.scrollTo({
            top: sectionPosition - headerHeight,
            behavior: 'smooth'
        });
    }
