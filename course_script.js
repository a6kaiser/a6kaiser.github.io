/* course_script.js */

/* Toggle Sidebar Function */
function togglesidebar() {
    var content = document.getElementById("content");
    var sidebarButton = document.getElementById("toggleButtonsidebar");
    var contentButton = document.getElementById("toggleButtonContent");

    content.classList.toggle("expanded"); // Expand/collapse the content area

    // Toggle aria-expanded attribute
    var isExpanded = content.classList.contains("expanded");
    sidebarButton.setAttribute('aria-expanded', !isExpanded);
    contentButton.setAttribute('aria-expanded', isExpanded);

    // Toggle button visibility based on sidebar state
    if (isExpanded) {
        sidebarButton.style.display = 'none'; // Hide the sidebar button

        // Show the content toggle button after the transition
        setTimeout(function() {
            contentButton.style.display = 'block'; // Show content button
        }, 300); // 300ms matches the CSS transition duration
    } else {
        // Hide the content toggle button and show the sidebar button
        contentButton.style.display = 'none'; // Hide content button
        sidebarButton.style.display = 'block'; // Show the sidebar button
    }
}

/* Initialize ClipboardJS for Copy Buttons */
document.addEventListener('DOMContentLoaded', function () {
    var clipboard = new ClipboardJS('.copy-button', {
        target: function(trigger) {
            var targetSelector = trigger.getAttribute('data-clipboard-target');
            return document.querySelector(targetSelector);
        }
    });

    // Success Feedback
    clipboard.on('success', function(e) {
        var originalText = e.trigger.textContent;
        e.trigger.textContent = 'Copied!';
        e.trigger.disabled = true;
        setTimeout(function() {
            e.trigger.textContent = 'Copy';
            e.trigger.disabled = false;
        }, 2000);
        e.clearSelection();
    });

    // Error Feedback
    clipboard.on('error', function(e) {
        var originalText = e.trigger.textContent;
        e.trigger.textContent = 'Error';
        e.trigger.disabled = true;
        setTimeout(function() {
            e.trigger.textContent = 'Copy';
            e.trigger.disabled = false;
        }, 2000);
    });
});

/* Smooth Scrolling for TOC Links */
document.querySelectorAll('.sidebar a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            const headerOffset = 70; // Height of the top banner
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

/* Initialize Collapsible Sections */
document.querySelectorAll('.collapsible-button').forEach(button => {
    button.addEventListener('click', function() {
        const content = this.nextElementSibling;
        const isExpanded = this.getAttribute('aria-expanded') === 'true';

        this.setAttribute('aria-expanded', !isExpanded);
        if (isExpanded) {
            content.style.display = 'none';
        } else {
            content.style.display = 'block';
        }
    });
});

/* Active TOC Link Highlighting */
document.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('h2, h3');
    const tocLinks = document.querySelectorAll('.sidebar a');
    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop <= 80) { // Adjusted threshold considering the top banner
            currentSection = section.getAttribute('id');
        }
    });

    tocLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === currentSection) {
            link.classList.add('active');
        }
    });
});
