package productservice.controller; // O org.example.polyglot si ese es tu groupId

import productservice.entity.Product;
import productservice.repository.ProductRepository;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*; // Importa todas las anotaciones necesarias

import java.util.List;
import java.util.Optional;

/**
 * Controlador REST para gestionar los recursos de Productos.
 * Expone los endpoints bajo la ruta base "/products".
 * Asume que el API Gateway eliminará un prefijo (ej. /api) antes de reenviar aquí.
 */
@RestController
@RequestMapping("/products") // Define la ruta base para todos los métodos en esta clase
public class ProductController {

    private final ProductRepository productRepository;

    // Inyección por constructor (Recomendado sobre @Autowired en campos)
    public ProductController(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    /**
     * Obtiene todos los productos.
     * Mapeado a GET /products
     * @return ResponseEntity con la lista de productos o vacío si no hay.
     */
    @GetMapping // Mapea a la raíz de la clase ("/products")
    public ResponseEntity<List<Product>> getAllProducts() {
        List<Product> products = productRepository.findAll();
        return ResponseEntity.ok(products);
    }

    /**
     * Obtiene un producto específico por su ID.
     * Mapeado a GET /products/{id}
     * @param id El ID del producto a buscar.
     * @return ResponseEntity con el producto si se encuentra, o 404 Not Found si no.
     */
    @GetMapping("/{id}") // Mapea a "/products/{id}"
    public ResponseEntity<Product> getProductById(@PathVariable Long id) {
        Optional<Product> product = productRepository.findById(id);
        return product.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    /**
     * Crea un nuevo producto.
     * Mapeado a POST /products
     * @param product El producto a crear, recibido en el cuerpo de la petición.
     * @return ResponseEntity con el producto creado y estado 201 Created.
     */
    @PostMapping // Mapea a la raíz de la clase ("/products")
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        // Asegurarse de que no se intente crear con un ID existente
        product.setId(null);
        Product savedProduct = productRepository.save(product);
        // Devuelve el producto guardado (que ahora tendrá un ID) y el estado CREATED
        return ResponseEntity.status(HttpStatus.CREATED).body(savedProduct);
    }

    /**
     * Actualiza un producto existente por su ID.
     * Mapeado a PUT /products/{id}
     * @param id El ID del producto a actualizar.
     * @param productDetails Los nuevos detalles del producto recibidos en el cuerpo.
     * @return ResponseEntity con el producto actualizado, o 404 Not Found si el ID no existe.
     */
    @PutMapping("/{id}") // Mapea a "/products/{id}"
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product productDetails) {
        // Busca el producto existente
        return productRepository.findById(id)
                .map(existingProduct -> { // Si existe...
                    // Actualiza los campos
                    existingProduct.setName(productDetails.getName());
                    existingProduct.setPrice(productDetails.getPrice());
                    // Guarda los cambios y devuelve el producto actualizado
                    Product updatedProduct = productRepository.save(existingProduct);
                    return ResponseEntity.ok(updatedProduct);
                })
                .orElseGet(() -> ResponseEntity.notFound().build()); // Si no existe, devuelve 404
    }

    /**
     * Elimina un producto por su ID.
     * Mapeado a DELETE /products/{id}
     * @param id El ID del producto a eliminar.
     * @return ResponseEntity con estado 204 No Content si se elimina, o 404 Not Found si no existe.
     */
    @DeleteMapping("/{id}") // Mapea a "/products/{id}"
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        // Verifica si el producto existe antes de intentar borrar
        if (productRepository.existsById(id)) {
            productRepository.deleteById(id);
            // Devuelve No Content (éxito sin cuerpo)
            return ResponseEntity.noContent().build();
        } else {
            // Devuelve Not Found si no existe
            return ResponseEntity.notFound().build();
        }
    }
}