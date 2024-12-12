// script.js

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    document.querySelector(".openbtn").style.display = "none"; // Hide the button
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
    document.querySelector(".openbtn").style.display = "block"; // Show the button
}
// Mobile Menu Toggle
const menuToggle = document.querySelector('.menu-toggle');
const menuNav = document.querySelector('.menu-nav');
if (menuToggle && menuNav) {
    menuToggle.addEventListener('click', () => {
        menuNav.classList.toggle('open');
    });
}

$(document).ready(function () {

    var csrf_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
    // searching
    $('.search-form').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        var query = $('.search-field').val(); // Get the search query
        window.location.href = '/search_results?q=' + query; // Redirect to search results page
    });

    // Initialize favorite count from session storage
    var favoriteCount = sessionStorage.getItem('favoriteCount') || 0;
    $('#favorite-product-count').text(favoriteCount);

        // Attach click event listener to the favorite buttons
        
    // Add to Cart Button Click Handler
   $(document).on('click', '.add-to-cart-btn', function (e) {
        e.preventDefault();
        const itemId = $(this).data('item-id');

        $.ajax({
            url: `/add_to_cart/${itemId}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ item_id: itemId }),
            success: function (response) {
                updateCartIcon(response.cart_count); // Update cart icon count
                alert(response.message);
            },
            error: function (error) {
                console.error('Error:', error);
                alert('Failed to add item to cart.');
            }
        });
    });

    // Remove Item from Cart Click Handler
    $(document).on('click', '.remove-from-cart-btn', function (e) {
        e.preventDefault();
        const cartId = $(this).data('cart-id');

        $.ajax({
            url: `/remove_from_cart/${cartId}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ cart_id: cartId }),
            success: function (response) {
                updateCartIcon(response.cart_count); // Update cart icon count
                updateCartSubtotal(response.new_subtotal); // Update cart subtotal
                alert(response.message);
            },
            error: function (error) {
                console.error('Error:', error);
                alert('Failed to remove item from cart.');
            }
        });
    });
});
// Helper to Get CSRF Token
function getCSRFToken() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]');
    return csrfToken ? csrfToken.content : '';
}

// Update Cart Icon
function updateCartIcon(count) {
    const cartIcon = document.querySelector('#cart-count');
    if (cartIcon) {
        cartIcon.textContent = count;
    }
}

// Update Cart Subtotal
function updateCartSubtotal(newSubtotal) {
    const subtotalElement = document.querySelector('#cart-subtotal');
    if (subtotalElement) {
        subtotalElement.textContent = `$${newSubtotal}`;
    }
}
//  ---------------- FAVORITES --------------------
$(document).ready(function() {
    $('.favorite-button').click(function() {
      var itemId = $(this).data('item-id');
      var button = $(this);
      var isFavorite = $(this).data('favorite'); // Get initial favorite status
  
      $.ajax({
        url: '/toggle_favorite/' + itemId,
        type: 'POST',
        success: function(response) {
          if (response.success) {
            // Toggle the data-favorite attribute and button appearance
            button.data('favorite', !isFavorite);
            if (response.is_favorite) {
              button.find('.favorite-icon path').attr('fill', '#EB584E');
            } else {
              button.find('.favorite-icon path').attr('fill', '#fff');
            }
  
            // If on favorites page and item was unfavorited, remove its card
            if (window.location.pathname.endsWith('/favorites') && !response.is_favorite) {
              button.closest('.col-md-4').remove();
            }
          } else {
            alert(response.message);
          }
          updateFavoriteCount(); 
        },
        error: function(error) {
          console.log(error);
          alert('Failed to update favorite status.');
        }
      });
    });
  });

  function updateFavoriteCount() {
    $.ajax({
      url: '/get_favorite_count',  // Replace with your actual route
      type: 'GET',
      success: function(response) {
        $('#favorite-product-count').text(response.count);
      },
      error: function(error) {
        console.log(error);
      }
    });
  }
  
  // Call this function on page load and whenever the favorites list changes
  $(document).ready(function() {
    updateFavoriteCount();
  });

// ---------------- CANCEL ORDER --------------------

 $(document).ready(function() {
    $('.cancel-order-btn').click(function() {
        const orderId = $(this).data('order-id');

        if (confirm("Are you sure you want to cancel this order?")) {
            $.ajax({
                url: '/cancel_order/' + orderId,
                type: 'POST',
                headers: {
                    'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')
                },
                success: function(response) {
                    alert("Order cancelled successfully.");
                    location.reload(); // Refresh the page to reflect changes
                },
                error: function(xhr) {
                    alert("Failed to cancel the order. Please try again.");
                }
            });
        }
    });
});
