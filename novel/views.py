from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Publisher,Author,Book
from datetime import datetime, timedelta

# Create your views here.
def author_form(request):

    if request.method == 'POST':
        salutation=request.POST['salutation']
        f_name=request.POST['first_name']
        l_name=request.POST['last_name']
        email=request.POST['email']
        bio=request.POST['bio']
        birth_date=request.POST['birth_date']
        picture=request.FILES.get('profile_picture',None)

        auth=Author(salutation=salutation,first_name=f_name,last_name=l_name,email=email,bio=bio,birth_date=birth_date,profile_picture=picture)
        auth.save()

        return redirect('book')
        
    return render(request,'author.html')


def book_form(request):
    all_pub=Publisher.objects.all()
    all_auth=Author.objects.all()

    if request.method == 'POST':
        title=request.POST['title']
        aname=request.POST['author_id']
        print(f" aname mein kya aara hai .............",aname)
        aname_fetched=Author.objects.get(id=aname)
        print(f"  pname fetched mei kya aara hai n...................",aname_fetched)
        pname=request.POST['publisher_id']
        print(f" pname mei kya aara hai.............",pname)
        pname_fetched=Publisher.objects.get(id=pname)
        print(f" pname fetched mein kya aara hai bata ",pname_fetched)
        date=request.POST['publication_date']
        isbn=request.POST['isbn']
        genre=request.POST['genre']
        price=request.POST['price']
        pages=request.POST['pages']
        language=request.POST['language']
        stock=request.POST['stock_quantity']
        image=request.FILES.get('cover_image',None)


        book=Book(title=title,publisher_id=pname_fetched,author_id=aname_fetched,publication_date=date,isbn=isbn,genre=genre,price=price,pages=pages,
             language=language,stock_quantity=stock,cover_image=image)
        book.save()

    context={
        'pub':all_pub,
        'auth':all_auth,
    }


    return render(request,'book.html',context)

def publisher_form(request):

    pub = None 

    if request.method == 'POST':
        p_name = request.POST.get('pname', '').strip()
        p_city=request.POST['city']
        p_state=request.POST['state']
        p_country=request.POST['country']
        p_website=request.POST['website']
        p_year=request.POST['established_year']
        p_number=request.POST['contact_number']
        p_address=request.POST['address']
        p_active = request.POST.get('is_active') == 'on'
        
        pub=Publisher(name=p_name,address=p_address,city=p_city,state=p_state,country=p_country,website=p_website,established_year=
                  p_year,contact_number=p_number,is_active=p_active)
        pub.save()

        return redirect('author') 


    return render(request,'publisher.html', {'pub': pub})


def all_books(request):
    all_books=Book.objects.all()
    context={
        'sabhi_books':all_books
    }
    return render(request,'all_books.html',context)


def auth_details(request):
    all_auth=Author.objects.all()
    author_details=[]

    for i in all_auth:
        author_name=i.first_name
        print(i.first_name)

        auth_book=Book.objects.filter(author_id=i.id)
        print(f"author ke books",auth_book)
        pub_auth_book=Book.objects.filter(author_id=i.id).values('publisher_id').distinct()
        print(f" kya aaya hai pub auth book mein ",pub_auth_book)
        no_of_auth_books=len(auth_book)
        print(no_of_auth_books)
        
        no_of_pub_books=len(pub_auth_book)
        print(no_of_pub_books)

        author_details.append({
            'n_publishers':no_of_pub_books,
             'n_authors':no_of_auth_books,
             'auth_names':author_name
        })

        context={
            'authors':author_details,
        }
        
    return render(request,'auth_details.html',context)

def auth_pub_more_than_2(request):
    all_auth = Author.objects.all()
    result = []

    for author in all_auth:
        books = Book.objects.filter(author_id=author.id).select_related('publisher')
        publishers = books.values('publisher_id', 'publisher_id__name').distinct()

        if publishers.count() >= 2:
            book_names = books.values_list('title', flat=True).distinct()
            publisher_names = publishers.values_list('publisher_id__name', flat=True)

            result.append({
                'author_name': f"{author.first_name} {author.last_name}",
                'books': list(book_names),
                'publishers': list(publisher_names),
            })

    context = {
        'more_than_two_filtered': result
    }

    return render(request, 'auth_pub_more_than_2.html', context)


# def auth_pub_more_than_2(request):
#     all_auth=Author.objects.all()
#     list1=[]

#     for i in all_auth:
#         author_names=i.first_name
#         print(i.first_name)

#         pub_auth_book=Book.objects.filter(author_id=i.id).values('publisher_id').distinct()
#         auth_pub_count=len(pub_auth_book)
#         if auth_pub_count >= 1 :
#                 author_name=i.first_name
#                 list1.append(author_name)
#                 print(list1)    
    
#     context={
#         'more_than_two_filtered':list1
#     }

#     return render(request,'auth_pub_more_than_2.html',context)


def pub_detail(request,id):
  
    single_pub_detail=Book.objects.filter(publisher_id=id)
    print(f" Publisher ki info : ......",single_pub_detail)

    context={
        'pub_detail':single_pub_detail,
    }
    return render(request,'pub_detail.html',context)



    # publishers = Publisher.objects.all()
    # for i in publishers:
    #     print(i)
    # single_pub_detail=Book.objects.filter(publisher_id=i.id)
    # print(f" Publisher ki info : ......",single_pub_detail)

    # context={
    #     'publishers' : single_pub_detail,
    # }
    
    return render(request, 'publisher_list.html',context)


from django.shortcuts import render
from django.http import JsonResponse
from .models import Book

def pattern_book_search(request):
    # Get the search query from the GET request
    search_query = request.GET.get('query', '')
    
    # Filter books based on the search query (case-insensitive)
    if search_query:
        pattern_books = Book.objects.filter(title__istartswith=search_query)
    else:
        pattern_books = Book.objects.all()  # Return all books if no query
    
    # Check if the request is AJAX for dynamic updates
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        books_list = [
            {
                'title': book.title,
                'author': book.author_id.first_name if book.author_id else 'N/A',
                'publisher': book.publisher_id.name if book.publisher_id else 'N/A',
                'publication_date': str(book.publication_date) if book.publication_date else 'N/A'
            }
            for book in pattern_books
        ]
        return JsonResponse({'books': books_list})
    
    context = {
        'pattern_search': pattern_books,
        'search_query': search_query
    }
    return render(request, 'pattern_search.html', context)



from django.shortcuts import render
from .models import Author, Publisher, Book
from django.db.models import Count

def auth_pub_more_than_5(request):
    # Group books by author and publisher, and filter where count >= 2
    books_grouped = (Book.objects.values('author_id', 'publisher_id')
                     .annotate(book_count=Count('id'))
                     .filter(book_count__gte=2))
    
    result = []
    for group in books_grouped:
        author = Author.objects.get(id=group['author_id'])
        publisher = Publisher.objects.get(id=group['publisher_id'])
        books = Book.objects.filter(author_id=author, publisher_id=publisher)
        result.append({
            'author': author,
            'publisher': publisher,
            'books': books,
        })

    context = {
        'auth_pub_more_than_2': result
    }
    return render(request, 'specific_filtered.html', context)




# from django.db.models import Count
# Ye Count ek aggregate function hai jise tu SQL ke COUNT(*) ki tarah samajh sakta hai. Iska kaam hai kisi cheez ki ginti karna 
# — jaise kitni books hain ek author ke paas.

# ✅ Yeh main line hai:
# python
# Copy
# Edit
# books_grouped = (Book.objects.values('author_id', 'publisher_id')
#                  .annotate(book_count=Count('id'))
#                  .filter(book_count__gte=2))
# Samjho step-by-step:
# 🔹 Book.objects.values('author_id', 'publisher_id')
# Ye kya karta hai?

# Ye Book table ka raw data laata hai sirf author_id aur publisher_id wale columns ka.

# Jaise SQL mein SELECT author_id, publisher_id FROM book;

# Ye basically bolega: “har unique combination of author + publisher do mujhe”.

# Example output ho sakta hai:

# python
# Copy
# Edit
# [
#  {'author_id': 1, 'publisher_id': 2},
#  {'author_id': 1, 'publisher_id': 2},
#  {'author_id': 3, 'publisher_id': 1},
#  {'author_id': 1, 'publisher_id': 2},
# ]
# 🔹 .annotate(book_count=Count('id'))
# Ab yeh har author_id + publisher_id group mein count karega kitni books hain.

# Count('id') matlab har group mein kitni books hain uski ginti.

# annotate() ka kaam hota hai grouping ke baad additional info (like sum, count, avg) lagana.

# Example output:

# python
# Copy
# Edit
# [
#  {'author_id': 1, 'publisher_id': 2, 'book_count': 3},
#  {'author_id': 3, 'publisher_id': 1, 'book_count': 1},
# ]
# 🔹 .filter(book_count__gte=2)
# gte matlab greater than or equal to.

# book_count__gte=2 bolega: "Mujhe wahi groups chahiye jahan kam se kam 2 books likhi gayi hoin is author + publisher combo ke saath."

# Final result:

# python
# Copy
# Edit
# [
#  {'author_id': 1, 'publisher_id': 2, 'book_count': 3},
# ]
# ✅ Ab ye part:
# python
# Copy
# Edit
# for group in books_grouped:
#     author = Author.objects.get(id=group['author_id'])
#     publisher = Publisher.objects.get(id=group['publisher_id'])
# Samjho group mein kya hai:
# Har group ek dictionary hai jisme hai:

# python
# Copy
# Edit
# {
#  'author_id': 1,
#  'publisher_id': 2,
#  'book_count': 3
# }
# Tu yahan group['author_id'] use karke Author model se id=1 wala author fetch kar raha hai.

# Waise hi group['publisher_id'] se Publisher model se id=2 wala publisher la raha hai.

# ✅ Ab last line:
# python
# Copy
# Edit
# books = Book.objects.filter(author_id=author, publisher_id=publisher)
# Iska matlab: "Ab mujhe woh sari books la de jahan ye author aur ye publisher dono involved hain."

# ✅ Finally ye append ho raha list mein:
# python
# Copy
# Edit
# result.append({
#     'author': author,
#     'publisher': publisher,
#     'books': books,
# })
# To tu context mein ek list bhej raha hai jisme har element mein:

# author object

# publisher object

# unki joint books queryset hai.



# Concept	                                   Matlab
# values()	               Sirf kuch fields extract karna, group banane ke liye
# annotate()	            Grouped result ke saath calculated field add karna (jaise count)
# Count()	                   Aggregate function jaise SQL COUNT(*)
# book_count__gte=2	             Sirf un groups ko filter karo jahan count ≥ 2 ho
# group['author_id']	         Dictionary ke andar author_id nikalna


# ----------------------------------------------------------------------------------------------------------------------------------------



def pub_specific_duration(request):
    today=datetime.today()
    three_days_ago= today - timedelta(days=3)
    publisher=Publisher.objects.all()
    print(publisher)   # ye query set ek object fetch karega  isliye jab book mein compare karege to i.id likehge 

        
    print(f"Today's date : {today.strftime('%Y-%m-%d')}")
    print(f"Date 3 days ago : {three_days_ago.strftime('%Y-%m-%d')}")

    books_data=[]

    for i in publisher:
        books=Book.objects.filter(publisher_id=i.id,publication_date__range=(three_days_ago,today))
        print(books)
        print({i.name})


        for book in books:
            print({book.title},{book.publication_date.strftime('%Y-%m-%d')})
            
        books_data.append((i,books))
       
        
    context={
            'books_data':books_data
        }

    return render(request,'pub_specific_duration.html',context)







# def auth_pub_more_than_5(request):
#     authors=Author.objects.all()
#     publisher=Publisher.objects.all()
#     list=[]

#     for i in authors:
#         print(i)
#         for j in publisher:
#             print(j)
#             books=Book.objects.filter(author_id=i.id,publisher_id=j.id)
#             print(books)
#             if len(books)>=2 :
#                 author=i.first_name
#                 list.append(author)

#         context={
#             'auth_pub_more_than_five':list
#         }

#     return render(request,'specific_filtered.html',context)










# def pattern_book_search(request):
#     pattern_books=Book.objects.filter(title__startswith="2")
#     print(pattern_books)
    
#     context={
#         'pattern_serach':pattern_books
#     }
#     return render(request,'pattern_search.html',context)   








# from django.shortcuts import render
# from .models import Book
# from django.http import JsonResponse

# def pattern_book_search(request):
    # Get the search query from the GET request
    # search_query = request.GET.get('query', '')
    
    # Filter books based on the search query (case-insensitive)
    # if search_query:
    #     pattern_books = Book.objects.filter(title__istartswith=search_query)
    # else:
        # pattern_books = Book.objects.all()  # Return all books if no query
    
    # For debugging, you can print the filtered books
    # print(pattern_books)
    
    # Check if the request is AJAX for dynamic updates
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     books_list = [{'title': book.title, 'id': book.id} for book in pattern_books]
    #     return JsonResponse({'books': books_list})
    
    # context = {
    #     'pattern_search': pattern_books,
    #     'search_query': search_query
    # }
    # return render(request, 'pattern_search.html', context)