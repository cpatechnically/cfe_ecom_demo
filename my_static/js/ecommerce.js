$(document).ready(function(){
    // contact form handler
    console.log("Contact form handler")
    let contactForm = $(".contact-form")
    let contactFormMethod = contactForm.attr("method")
    let contactFormEndpoint = contactForm.attr("action")

    function displaySubmitting(submitBtn, defaultText, doSubmit){

      if (doSubmit){
        submitBtn.addClass("disabled")
        submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending....")  
      } else {
        submitBtn.removeClass("disabled")
        submitBtn.html(defaultText)  
        
      }
    }
    contactForm.submit(function(e){
      e.preventDefault()

      let contactFormSubmitBtn = contactForm.find("[type='submit']")
      let contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
      let contactFormData = contactForm.serialize()
      let thisForm = $(this)

      displaySubmitting(contactFormSubmitBtn,"",true)
      $.ajax({
        url: contactFormEndpoint,
        method: contactFormMethod,
        data: contactFormData,
        success: function(data){
          contactForm[0].reset()
          $.alert({
            title: "Success!",
            //can use data.message b/c the view function is returning json dictionary with a {"message":"...."}
            content: "Thank you for your submission!",//data.message,
            theme: "modern",
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
          }, 500)
        },
        error: function(error){
          console.log(error)
          let jsonData = error.responseJSON
          let msg = ""
          $.each(jsonData, function(key,value){
            msg += key + ": " + value[0].message + "<br/>"
          })
          $.alert({
            title: "Oops!",
            content: msg,
            theme: "modern",
          })
          setTimeout(function(){
            displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnTxt,false)
          }, 500) 
        }
      })
    })
    


    // Auto Search Form
    let searchForm = $(".search-form")
    let searchInput = searchForm.find("[name='q']") // input name='q'
    let typingTimer;
    let typingInterval = 500 // 1 second
    let searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(e){
      // executes when keys are released
      console.log(searchInput.val())
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(e){
      // executes when keys are pressed, USING BOTH TO CONFIRM SEARCH IS CLEARED OUT
      clearTimeout(typingTimer)
    })

    function displaySearch(){
      searchBtn.addClass("disabled")
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching....")
    }

    function performSearch(){
      displaySearch()
      let query = searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q=' + query
      }, 1000)
    }



    // Product Form Cart + Add Products
    let productForm = $('.form-product-ajax')

    function getOwnedProduct(productId, submitSpan){
      var actionEndpoint = '/orders/endpoint/verify/ownership/'
      var httpMethod = 'GET'
      var data = {
        product_id: productId
      }
  
      var isOwner;
      $.ajax({
          url: actionEndpoint,
          method: httpMethod,
          data: data,
          success: function(data){
            console.log(data)
            console.log(data.owner)
            if (data.owner){
              isOwner = true
              submitSpan.html("<a class='btn btn-warning' href='/library/'>In Library</a>")
            } else {
              isOwner = false
            }
          },
          error: function(erorr){
            console.log(error)
  
          }
      })
      return isOwner
      
    }
    $.each(productForm, function(index, object){
      var $this = $(this)
      var isUser = $this.attr("data-user")
      var submitSpan = $this.find(".submit-span")
      var productInput = $this.find("[name='product_id']")
      var productId = productInput.attr("value")
      var productIsDigital = productInput.attr("data-is-digital")
      
      if (productIsDigital && isUser){
        var isOwned = getOwnedProduct(productId, submitSpan)
      }
    })  

    productForm.submit(function(e){
      e.preventDefault();
      //console.log('form not sending')
      let thisForm = $(this)
      //let actionEndpoint = thisForm.attr("action");
      let actionEndpoint = thisForm.attr("data-endpoint");
      let httpMethod = thisForm.attr("method");
      let formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          console.log("success")
          //console.log(data)
          //console.log("added",data.added)
          //console.log("removed",data.removed)
          let submitSpan = thisForm.find(".submit-span")
          if (data.added){
            submitSpan.html("In Cart <button type='submit' class='btn btn-link'>Remove?</button>")
          } else {
            submitSpan.html("<button type='submit'  class='btn btn-success'>Add to cart</button>")
          }
          let navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)
          //console.log(submitSpan.html())
          let currentPath = window.location.href
          console.log(currentPath)
          if (currentPath.indexOf("cart") != -1) {
            refreshCart()
          }
        },
        error: function(errorData){
          //jQuery CONFIRM alery
          $.alert("An error occured")
          //Traditional Alert--- alert("An error occured")
          console.log("error")
          console.log(errorData)
        }
      })
    })
    function refreshCart(){
      console.log("in cart current")
      let cartTable = $(".cart-table")
      let cartBody = cartTable.find(".cart-body")
      //cartBody.html("<h1>Changed</h1>")
      let productRows = cartBody.find(".cart-product")
      let currentUrl = window.location.href;
      let refreshCartUrl = '/api/carts/'
      let refreshCartMethod = "GET";
      let data = {};
      $.ajax({ 
        url: refreshCartUrl,
        method: refreshCartMethod,
        data: data,
        success: function(data){
          console.log("Success",data)
          let hiddenCartItemRemoveForm = $(".cart-item-remove-form")
          if (data.products.length > 0){
            productRows.html(" ")
            i = data.products.length
            $.each(data.products,function(index,value){
              console.log(value)
              let newCartItemRemove = hiddenCartItemRemoveForm.clone()
              newCartItemRemove.css("display","block")
              newCartItemRemove.find(".cart-item-product-id").val(value.id)
              cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + 
                value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                //subtract i so counts down to zero
                i --
            })
            cartBody.find(".cart-subtotal").text(data.subtotal)
            cartBody.find(".cart-total").text(data.total)
          } else {
            //refresh the page
            window.location.href = currentUrl
          }
        },
        error: function(errorData){
          console.log("Error",errorData)
        }
      })
    }
  })