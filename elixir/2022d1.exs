defmodule Solution do
  def ex(filename, how_many) do
    contents = File.read!(filename)

    String.split(contents, "\n\n")
    |> Enum.map(fn x ->
      String.split(x)
      |> Enum.map(&String.to_integer/1)
      |> Enum.reduce(0, fn acc, x -> acc + x end)
    end)
    |> Enum.sort(:desc)
    |> Enum.take(how_many)
    |> Enum.sum()
  end

  def ex1(filename) do
    ex(filename, 1)
  end

  def ex2(filename) do
    ex(filename, 3)
  end
end

IO.write("ex1: #{Solution.ex1("input.txt")}\n")
IO.write("ex2: #{Solution.ex2("input.txt")}\n")
