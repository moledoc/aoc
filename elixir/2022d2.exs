defmodule Solution do
  def ex1(filename) do
    points = %{"X" => 1, "Y" => 2, "Z" => 3}
    draw = %{"X" => "A", "Y" => "B", "Z" => "C"}
    win = %{"Z" => "B", "Y" => "A", "X" => "C"}
    contents = File.read!(filename)

    res =
      contents
      |> String.trim()
      |> String.split("\n")
      |> Enum.map(fn x -> String.split(x, " ") |> List.to_tuple() end)
      |> Enum.map(fn {op, u} ->
        cond do
          win[u] == op -> points[u] + 6
          draw[u] == op -> points[u] + 3
          true -> points[u] + 0
        end
      end)
      |> Enum.sum()

    res
  end

  def ex2(filename) do
    points = %{"X" => 1, "Y" => 2, "Z" => 3}
    lose = %{"A" => "Z", "B" => "X", "C" => "Y"}
    draw = %{"A" => "X", "B" => "Y", "C" => "Z"}
    win = %{"B" => "Z", "A" => "Y", "C" => "X"}
    contents = File.read!(filename)

    res =
      contents
      |> String.trim()
      |> String.split("\n")
      |> Enum.map(fn x -> String.split(x, " ") |> List.to_tuple() end)
      |> Enum.map(fn {op, u} ->
        cond do
          # lose
          u == "X" -> points[lose[op]] + 0
          # draw
          u == "Y" -> points[draw[op]] + 3
          # win
          u == "Z" -> points[win[op]] + 6
        end
      end)
      |> Enum.sum()

    res
  end
end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
