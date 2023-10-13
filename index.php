<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tổng hợp job fresher từ Facebook</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous" />
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

    <style>
        .post {
            max-height: 500px;
            overflow: auto;

        }

        .post::-webkit-scrollbar {
            width: 10px;
        }

        .post::-webkit-scrollbar-thumb {
            background-color: #ddd;
            border-radius: 10px;
        }


        .post::-webkit-scrollbar-thumb:hover {
            background-color: #555;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1 class="my-5 text-center">Tổng hợp job fresher từ Facebook</h1>

        <div id="post-container">
            <?php
            $jsonData = file_get_contents('post_data.json');
            $data = json_decode($jsonData, true);

            $count = 0;
            foreach ($data as $post) {
                if ($count % 3 == 0) {
                    echo '<div class="row">';
                }
                echo '<div class="col-md-4 mb-3 post">';
                echo '<div class="card">';
                echo '<div class="card-body">';
                echo '<h5 class="card-title">' . $post['name'] . '</h5>';
                echo '<h6 class="card-subtitle mb-2 text-muted">' . $post['time'] . '</h6>';
                echo '<div class="post-text">';
                echo '<p class="card-text">' . $post['post_text'] . '</p>';
                echo '</div>';
                echo '<a href="' . $post['post_link'] . '" class="card-link">Xem chi tiết</a>';
                echo '</div>';
                echo '</div>';
                echo '</div>';
                if (($count + 1) % 3 == 0 || ($count + 1) == count($data)) {
                    echo '</div>';
                }
                $count++;
            }
            ?>
        </div>
    </div>

</body>

</html>