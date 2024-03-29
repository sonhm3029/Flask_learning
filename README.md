# Flask_learning

## 1. Application

Một app Flask đơn giản như sau:

```Python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World’

if __name__ == '__main__':
   app.run()
```

Trong đó `Flask` constructors nhận vào tên của `current module` qua tham số `__name__`.

`route()` function để define route cho app. Cú pháp như sau:

```Python
@app.route(rule, options)
```

- `rule` là tên route
- `options` là list các parameters truyền vào `Rule` object

Cuối cùng là chạy server lên với syntax:

```Python
app.run(host, port,debug,options)
```

Chú thích tham số:

Tham số | Description
--------|------------
host | Nếu không truyền vào thì default host là `127.0.0.1`(localhost). Truyền vào `0.0.0.0` để chạy máy chủ riêng.
port | port chạy server, nếu không truyền vào thì default là 5000
debug | Default là false ở chế độ này nếu có thay đổi trong code thì phải kill terminal đi khởi động lại server. Khi set sang `True` thì server sẽ tự động lắng nghe các thay đổi trong code và tự động khởi động lại.
options | To be forwarded to underlying Werkzeug server.

## 2. Routing

Như với ví dụ đơn giản thứ 1 thì route được define như sau:

```Python
@app.route('/route_name')
def route_func():
   ...smt
```

Để cho clean hơn thì ta có cách viết khác như sau:

```Python
app.add_url_rule('/route_name',route_func )
```

## 3. Route Params

Để sử dụng dynamic route với params thay đổi, ta có:

```Python
@app.route('/profile/<id>')
def profile(id)
   return 'Hello %s' % id
```

Với ví dụ trên thì phần thay đổi trong route là `<id>`, route này sẽ nhận các các giá trị id khác nhau và được truyền làm tham số trong `route function`. Chú ý rằng ở đây bắt buộc phải có tham số truyền vào `route function` và tham số này bắt buộc phải cùng tên với `slug` để ở `route` đã define. Trong trường hợp này là `id`.

Ta có thể định nghĩa kiểu dữ liệu cho `params`. Kiểu `int`, `float` hoặc `path`.

- Default là kiểu `path` tức param có thể mang giá trị gồm các kí tự

- Kiểu `int`, param chỉ nhận tham số kiểu `int`, ví dụ nếu cho vào param là `/profile/2.0` hoặc `/profile/a` => Sẽ lỗi

- Kiểu `float`, param chỉ nhận tham số kiểu `float` => nếu cho vào param là `/profile/2` hoặc `/profile/a` => Sẽ lỗi

```Python
@app.route('/profile/<int:id>')   #int
@app.route('/profile/<float:id>') # float
@app.route('/profile/<id>')       #path
```

Chú ý nếu như define route như sau:

```Python
@app.route('/home')
@app.route('/home/')
```

Đối với kiểu đầu tiên. Khi ta chỉ có thể truy cập server thông quá route chính xác là `/home`, nếu như truy cập bằng `/home/` => sẽ lỗi

Đối với kiểu thứ 2. Ta có thể truy cập server bằng cả 2 route là `/home` hoặc `/home/` thì đều như nhau.

## 4. URL building

```Python
from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))

if __name__ == '__main__':
   app.run(debug = True)
```

Như vậy khi vào `route` là `/user/admin` => redirect sang trang `/admin`.

Khi vào `route` là `/user/smt` => redirect sang trang `/guest/smt`.

## 5. HTTP Methods

| 1 | GET Sends data in unencrypted form to the server. Most common method.                             |
|---|---------------------------------------------------------------------------------------------------|
| 2 | HEAD Same as GET, but without response body                                                       |
| 3 | POST Used to send HTML form data to server. Data received by POST method is not cached by server. |
| 4 | PUT Replaces all current representations of the target resource with the uploaded content.        |
| 5 | DELETE Removes all current representations of the target resource given by a URL                  |

Default, Flask route sẽ dùng `GET` request.

Ví dụ sử dụng http method:

```Python
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)
```

## 6. Template

Thông thường ngoài return các giá trị Number, string, json... Thì ta có thể trả về cả html

```Python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
   return '<html><body><h1>Hello World</h1></body></html>'

if __name__ == '__main__':
   app.run(debug = True)
```

Tuy nhiên việc return cả chuỗi html  như trên là không nên.

Flask cho phép ra render ra các template và truyền data vào template để render ra giao diện với template engine là `Jinja2`

```Python
from flask import Flask
app = Flask(__name__)

@app.route('/hello/<user>')
def hello_name():
   return render_template('hello.html',name=user)

if __name__ == '__main__':
   app.run(debug = True)
```

Cấu trúc thư mục để sử dụng template như sau:

```cmd
.
|
|---|Hello.py
|---|templates
    |
    |--hello.html
```

Trong file `Hello.py`

```html
<!doctype html>
<html>
   <body>
   
      <h1>Hello {{ name }}!</h1>
      
   </body>
</html>
```

`Jinja2` sử dụng một số quy chuẩn để render data vào html:

- `{% ... %}` for Statements
- `{{ ... }}` for Expressions to print to the template output
- `{# ... #}` for Comments not included in the template output
- `# ... ##` for Line Statements

### Ví dụ sử dụng if...else:

```Python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello/<int:score>')
def hello_name(score):
   return render_template('hello.html', marks = score)

if __name__ == '__main__':
   app.run(debug = True)
```

Trong file `hello.html`

```html
<!doctype html>
<html>
   <body>
      {% if marks>50 %}
         <h1> Your result is pass!</h1>
      {% else %}
         <h1>Your result is fail</h1>
      {% endif %}
   </body>
</html>
```

### Ví dụ sử dụng for loop:

```Python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

if __name__ == '__main__':
   app.run(debug = True)
```

Trong file `result.html`

```html
<!doctype html>
<html>
   <body>
      <table border = 1>
         {% for key, value in result.items() %}
            <tr>
               <th> {{ key }} </th>
               <td> {{ value }} </td>
            </tr>
         {% endfor %}
      </table>
   </body>
</html>
```

## 7. Static file

## 8 .Request Object

Các attributes quan trọng của `request` gồm :

- `Form` − dict object các trường và data của form trong post method

- `args` − parsed content của query string (các data gửi phân cách bởi ? )

- `Cookies` − dict object giữ các trường và giá trị của cookies

- `files` − data pertaining to uploaded file.

- `method` − method của request hiện tại